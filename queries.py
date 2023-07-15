import sys
import redis
from redis_lru import RedisLRU

from connect import create_connect
from models import Authors, Quotes


#  connect to Redis local server
client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client, default_ttl=60 * 20)


@cache
def do_name_query(query_author):
    result = []
    author = Authors.objects.get(fullname__istartswith=query_author)

    quotes = Quotes.objects(author=author)
    if quotes:
        print(f"Quotes by {author.fullname}:")
        for quote in quotes:
            result.append(quote.quote)
        return result
    else:
        print("There are no quotes by this author.")


@cache
def do_tag_query(query_tag):
    result = []
    query_tag_list = query_tag.split(",")

    matching_quotes = Quotes.objects(tags__in=query_tag_list)  # Select from the database only those quotes which have the requested tags
    if matching_quotes:

        for quote in matching_quotes:
            one_quote = []

            one_quote.append(quote.author.fullname)  # add author's fullname
            one_quote.append([tag for tag in quote.tags if tag in query_tag_list])  # add tags
            one_quote.append(quote.quote)  # add quote

            result.append(one_quote)

        return result


def main():
    create_connect()

    while True:
        query = input().split(":")
        match query[0]:
            case "exit":
                sys.exit()

            case "name":
                quotes = do_name_query(query[1])
                [print(quote) for quote in quotes]
                print()

            case "tag" | "tags":
                result = do_tag_query("".join(query[1]))  # query is str again
                for quote in result:
                    print(f"Quote by {quote[0]}\nTag(s):", end=" ")
                    [print(tag, end=" ") for tag in quote[1]]
                    print(f"\n{quote[2]}\n")

            case _:
                print(f"\n[{query[0]}] Unknown command. Please, try again.\n")


if __name__ == '__main__':
    main()
