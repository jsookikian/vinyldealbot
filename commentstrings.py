def getCommentString(artists):
    comment = "**VinylDealBot**\n\nYou will now receive messages when the following go on sale:\n\n"
    for artist in artists:
        comment +=  artist + "\n\n"
    comment += "To get alerts, comment ```VinylDealBot Artist```\n\n"
    comment += "To remove alerts, comment ```VinylDealBot Remove Artist```\n\nSeparate multiple artists/albums with semicolons(;)"
    return comment

def getRemoveArtistsCommentString(artists):
    comment = "**VinylDealBot**\n\nYou will no longer receive messages for the following:\n\n"
    for artist in artists:
        comment +=  artist + "\n\n"
    comment += "To get alerts, comment ```VinylDealBot Artist```\n\n"
    comment += "To remove alerts, comment ```VinylDealBot Remove Artist]```\n\nSeparate multiple artists/albums with semicolons(;)"
    return comment

def getRemovedAllCommentString(artists):
    comment = "**VinylDealBot**\n\nYou will no longer receive messages for the following:\n\n"
    for artist in artists:
        comment +=  artist + "\n\n"
    comment += "To get alerts, comment ```VinylDealBot Artist```\n\n"
    comment += "To remove alerts, comment ```VinylDealBot Remove Artist```\n\nSeparate multiple artists/albums with semicolons(;)"
    return comment

def getShowAllCommentString(artists):
    comment = "**VinylDealBot**\n\nYou are currently signed up for alerts on the following:\n\n"
    for artist,created in artists:
        comment +=  artist + "\n\n"
    comment += "To get alerts, comment ```VinylDealBot Artist```\n\n"
    comment += "To remove alerts, comment ```VinylDealBot Remove Artist```\n\nSeparate multiple artists/albums with semicolons(;)"
    return comment

def get_template(artist, title, url, permalink):
    return '**VinylDealBot** on [r/VinylDeals](http://reddit.com/r/VinylDeals)\n\n' \
            + "[" + title + "](" + permalink + ")\n\n" \
            + url

def getUpdateString():
    comment = "**VinylDealBot**\n\nThere has been an update to the Vinyl Deal Bot\n\n "
    comment += "Now, you must use a semicolon (;) to separate your artists so now you can use artists with a comma in their name\n\n"
    comment += "Example:\n\n```VinylDealBot Crosby, Stills, and Nash; Tyler, The Creator; David Bowie```\n\n"
    comment += "To get alerts, comment ```VinylDealBot [Artist | Album ] ```\n\n"
    comment += "To remove alerts, comment ```VinylDealBot Remove [Artist | Album]```\n\nSeparate multiple artists/albums with semicolons (;)\n\n"
    comment += "Thank you for using Vinyl Deal Bot!"
    return comment
