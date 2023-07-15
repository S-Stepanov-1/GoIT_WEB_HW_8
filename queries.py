import sys

from connect import create_connect
from models import Authors, Quotes


def do_name_query(query_author):
    author = Authors.objects.get(fullname__istartswith=query_author)

    quotes = Quotes.objects(author=author)
    if quotes:
        print(f"Quotes by {author.fullname}:")
        for quote in quotes:
            print(quote.quote)
        print()
    else:
        print("There are no quotes by this author.")


def do_tag_query(query_tag):
    query_tag_list = query_tag.split(",")

    matching_quotes = Quotes.objects(tags__in=query_tag_list)
    if matching_quotes:

        for quote in matching_quotes:
            print(f"Quote by {quote.author.fullname}\nTag(s):", end=" ")
            [print(tag, end=" ") for tag in quote.tags if tag in query_tag_list]
            print(f"\n{quote.quote}\n")


def main():
    create_connect()

    while True:
        query = input().split(":")
        match query[0]:
            case "exit":
                sys.exit()
            case "name":
                do_name_query(query[1])
            case "tag" | "tags":
                do_tag_query("".join(query[1]))  # query is str again
            case _:
                print(f"\n[{query[0]}] Unknown command. Please, try again.\n")


if __name__ == '__main__':
    main()
