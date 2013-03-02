/*
 * Writetags: a very basig snippet to write ID3, OGG, ... tags with Taglib (libtag).
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Require: libtag1-dev (Debian)
 * Usage:   g++ writetags.cc -o writetags $(pkg-config --cflags --libs taglib)
 *
 * See http://taglib.github.com/api/
 *
 */

#include <iostream>
#include <iomanip>

#include <fileref.h>
#include <tag.h>

int main(int argc, char * argv[])
{
    if(argc == 1) {
        std::cerr << "Usage: " << argv[0] << " FILE [FILE...]" << std::endl;
        exit(1);
    }

    for(int i=1 ; i<argc ; i++) {

        char * file_name = argv[i];
        std::cout << file_name << std::endl;

        TagLib::FileRef file_ref(file_name);

        if(!file_ref.isNull() && file_ref.tag()) {

            TagLib::Tag * tag = file_ref.tag();

            tag->setTitle("My title");
            tag->setArtist("My artist");
            tag->setAlbum("My album");
            tag->setYear(2000);
            tag->setComment("My comment");
            tag->setTrack(1);
            tag->setGenre("My genre");

            file_ref.file()->save();

        }

    }

    return 0;
}

