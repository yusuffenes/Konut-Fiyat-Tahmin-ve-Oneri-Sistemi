def display_listings(listings):
    for i in range(0, len(listings), 2):
        listing1 = listings[i]
        print(f"Listing 1: {listing1['title']}, {listing1['url']}")
        if i + 1 < len(listings):
            listing2 = listings[i + 1]
            print(f"Listing 2: {listing2['title']}, {listing2['url']}")
        print("-" * 50) 
