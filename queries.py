import sys

from connect import create_connect
from models import Authors, Quotes


def do_name_query(query_author):
    author = Authors.objects.get(fullname=query_author).id

    quotes = Quotes.objects(author=author)
    if quotes:
        print(f"Quotes by {query_author}:")
        for quote in quotes:
            print(quote.quote)
        print()
    else:
        print("There are no quotes by this author.")


def do_tag_query(query_tag):
    all_quotes = Quotes.objects()

    if all_quotes:

        for quote in all_quotes:
            if query_tag in quote.tags:
                print(f"Quote by {quote.author.fullname}")
                print(quote.quote + "\n")


def do_many_tags_query(query_tags):
    pass


def main():
    create_connect()

    while True:
        query = input().split(":")
        match query[0]:
            case "exit":
                sys.exit()
            case "name":
                do_name_query(query[1])
            case "tag":
                do_tag_query(query[1])
            case "tags":
                do_many_tags_query(query[1:])
            case _:
                print("\nUnknown command. Please, try again.\n")


if __name__ == '__main__':
    main()
