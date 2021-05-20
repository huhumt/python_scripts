#!/usr/bin/env bash

composite_img()
{
    local img_name="$1"
    local img_name_path="${img_name%.*}"
    local img_tmp_filename="${img_name_path}_tmp.png"
    local img_target_filename="${img_name_path}_new.png"

    magick_path="C:\Program Files\ImageMagick-7.0.11-Q16-HDRI\magick.exe"
    # compile_project="\"$magick_path\" ./channel_mapping.png ./test_apl.png -set option:ww "%[fx:max(u.w,v.w)]" -set option:hh "%[fx:max(u.h,v.h)]" -resize "%[ww]x%[hh]" -background white -gravity center -append -quality 100 red_green.png"
    # compile_project="\"$magick_path\" base.png test_apl.png -background white -gravity center -append -quality 100 red_green.png"
    # compile_project="\"$magick_path\" convert base.png -resize 50% test_apl.png -gravity center -composite all_new.png"
    echo "resize $img_name to $img_tmp_filename"
    resize_img="\"$magick_path\" convert -resize 640x590\! -matte -channel a -evaluate set 35% +channel $img_name $img_tmp_filename"
    eval $resize_img
    echo "composite $img_tmp_filename with ./image/base.png to $img_target_filename"
    echo ""
    composite_img="\"$magick_path\" convert ./image/base.png $img_tmp_filename -gravity NorthWest -composite $img_target_filename"
    eval $composite_img
    rm -fr $img_tmp_filename
}

check_type()
{
    local par1=$1
    local support_type=( png jpeg jpg )
    local file_type="${par1##*.}"
    local type

    for type in ${support_type[@]}
    do
        if [ "$file_type" = "$type" ]
        then
            return 0
        fi
    done
    return 1
}

main()
{
    local png_list=$(ls "./image/generate_img/")

    for png_file in ${png_list[@]}
    do
        local full_png_name="./image/generate_img/$png_file"
        check_type $full_png_name

        if [ $? -eq 0 ]
        then
            composite_img $full_png_name
        fi
    done
}

main
