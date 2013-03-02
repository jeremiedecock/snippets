/*
 * Readtags: a very basig snippet to read ID3, OGG, ... tags with Taglib (libtag).
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Require: libtag1-dev (Debian)
 * Usage:   g++ readtags.cc -o readtags $(pkg-config --cflags --libs taglib)
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

        std::cout << std::endl << "******************** " << file_name << " ********************" << std::endl << std::endl;

        TagLib::FileRef file_ref(file_name);

        if(!file_ref.isNull() && file_ref.tag()) {

            TagLib::Tag * tag = file_ref.tag();

            std::cout << "--- TAGS ---" << std::endl;
            std::cout << "title   : \"" << tag->title()   << "\"" << std::endl;
            std::cout << "artist  : \"" << tag->artist()  << "\"" << std::endl;
            std::cout << "album   : \"" << tag->album()   << "\"" << std::endl;
            std::cout << "year    : \"" << tag->year()    << "\"" << std::endl;
            std::cout << "comment : \"" << tag->comment() << "\"" << std::endl;
            std::cout << "track   : \"" << tag->track()   << "\"" << std::endl;
            std::cout << "genre   : \"" << tag->genre()   << "\"" << std::endl;

        }

        if(!file_ref.isNull() && file_ref.audioProperties()) {

            TagLib::AudioProperties * properties = file_ref.audioProperties();

            int seconds = properties->length() % 60;
            int minutes = (properties->length() - seconds) / 60;

            std::cout << std::endl << "--- PROPERTIES ---" << std::endl;
            std::cout << "bitrate     : " << properties->bitrate() << std::endl;
            std::cout << "sample rate : " << properties->sampleRate() << std::endl;
            std::cout << "channels    : " << properties->channels() << std::endl;
            std::cout << "length      : " << minutes << ":" << std::setfill('0') << std::setw(2) << seconds << std::endl;

        }

    }

    return 0;
}

