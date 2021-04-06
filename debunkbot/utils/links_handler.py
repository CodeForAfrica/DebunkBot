from typing import Iterable, List

from debunkbot.models import Claim


def get_links(claims: Iterable[Claim]) -> List[str]:
    """
    Returns a list of links from all the claims that we have.
    """
    links = set()
    # This will most of the times get the cached claims so no network calls will be
    # made.
    for claim in claims:
        if not claim.rating:
            if claim.claim_first_appearance:
                url_link_p = remove_proto(claim.claim_first_appearance)
                current_filter = generate_filter(claim.claim_first_appearance)
                links.add(current_filter.strip())
            elif claim.claim_appearances:
                for claim_appearance in claim.claim_appearances:
                    url_link = claim_appearance
                    if url_link != "":
                        url_link_p = remove_proto(url_link)
                        if len(url_link_p) < 60:
                            links.add(url_link_p)
                            continue
                        current_filter = generate_filter(url_link)
                        links.add(current_filter.strip())
            elif claim.claim_phrase:
                links.add(claim.claim_phrase[:60])
            else:
                continue
    return list(links)


def remove_proto(url):
    url = url.split("://")[-1]
    return url


def generate_filter(url_link):
    url_link = url_link.split("://")[-1]
    url_link = url_link.split("www.")[-1]
    url_link = url_link.split("mobile.")[-1]
    url_link = url_link.split("web.")[-1]
    url_link = url_link.split("docs.")[-1]

    url_link = url_link.split("/")
    # Replace the . with a space
    domain_part = url_link[0].split(".")
    url_link = domain_part + url_link[1:]
    url_parts = " ".join(url_link)
    url_parts = " ".join(
        " ".join(
            " ".join(
                " ".join(" ".join(url_parts.split("?")).split(".")).split("=")
            ).split("&")
        ).split("-")
    )
    # Pick the first 60 words of the new url.
    all_parts = url_parts.split(" ")
    current_filter = ""
    for part in all_parts:
        if len(current_filter) < 60 and len(current_filter + part) < 60:
            current_filter += part + " "
        else:
            break
    current_filter = " ".join(current_filter.split("?"))
    return current_filter
