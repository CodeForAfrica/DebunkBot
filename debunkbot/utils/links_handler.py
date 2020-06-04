def get_links(source):
        """
            Returns a list of links from all the claims that we have.
        """
        links = []
        # This will most of the times get the cached claims so no network calls will be made.
        for claim in source.get_claims():
            if claim.claim_first_appearance:
                url_link = claim.claim_first_appearance
                if url_link != '' and not claim.rating:
                    url_link = url_link.split("://")[-1]
                    url_link = url_link.split("www.")[-1]
                    url_link = url_link.split("mobile.")[-1]
                    url_link = url_link.split("web.")[-1]
                    url_link = url_link.split("docs.")[-1]
                    
                    url_link = url_link.split("/")
                    # Replace the . with a space
                    domain_part = url_link[0].split('.')
                    url_link = domain_part+url_link[1:]
                    url_parts = ' '.join(url_link)
                    url_parts = ' '.join(' '.join(' '.join(' '.join(url_parts.split('?')).split('.')).split('=')).split('&'))
                    # Pick the first 60 words of the new url.
                    all_parts = url_parts.split(' ')
                    current_filter = ''
                    for part in all_parts:
                        if len(current_filter) < 60 and len(current_filter+part) < 60:
                            current_filter +=part+" "
                        else:
                            break
                    current_filter = ' '.join(current_filter.split('?'))
                    links.append(current_filter.strip())     
            elif claim.claim_phrase and not claim.rating:
                links.append(claim.claim_phrase[:60])
            else:
                # We don't have anything to tack on this claim
                continue
        return links
