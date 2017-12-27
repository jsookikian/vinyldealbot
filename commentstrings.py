def getCommentString(artists):
    comment = "**VinylDealBot**\n\nYou will now receive messages when the following go on sale:\n\n "
    for artist in artists:
        comment +=  artist + "\n\n"
    comment += "To get alerts, comment ```VinylDealBot [Artist | Album ] ```\n\n"
    comment += "To remove alerts, comment ```VinylDealBot Remove [Artist | Album]```\n\nSeparate multiple artists/albums with commas"
    return comment

def getRemoveArtistsCommentString(artists):
    comment = "**VinylDealBot**\n\nYou will no longer receive messages for the following:\n\n "
    for artist in artists:
        comment +=  artist + "\n\n"
    comment += "To get alerts, comment ```VinylDealBot [Artist | Album ] ```\n\n"
    comment += "To remove alerts, comment ```VinylDealBot Remove [Artist | Album]```\n\nSeparate multiple artists/albums with commas"
    return comment

def getRemovedAllCommentString(artists):
    comment = "**VinylDealBot**\n\nYou will no longer receive messages for the following:\n\n "
    for artist in artists:
        comment +=  artist + "\n\n"
    comment += "To get alerts, comment ```VinylDealBot [Artist | Album ] ```\n\n"
    comment += "To remove alerts, comment ```VinylDealBot Remove [Artist | Album]```\n\nSeparate multiple artists/albums with commas"
    return comment

def getShowAllCommentString(artists):
    comment = "**VinylDealBot**\n\nYou are currently signed up for alerts on the following:\n\n "
    for artist,created in artists:
        comment +=  artist + "\n\n"
    comment += "To get alerts, comment ```VinylDealBot [Artist | Album ] ```\n\n"
    comment += "To remove alerts, comment ```VinylDealBot Remove [Artist | Album]```\n\nSeparate multiple artists/albums with commas"
    return comment

def get_template(artist, title, url, permalink):
    return '**VinylDealBot** on [r/VinylDeals](http://reddit.com/r/VinylDeals)\n\n' \
            + "[" + title + "](" + permalink + ")\n\n" \
            + url