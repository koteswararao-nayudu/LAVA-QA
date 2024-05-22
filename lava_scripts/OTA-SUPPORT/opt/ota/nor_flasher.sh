#!/bin/bash

partition=$1
action=$2
write_file=$3
erase_block_num=$4
MTD0_SIZE=512
MTD1_SIZE=128
MTD2_SIZE=128
MTD3_SIZE=5376
MTD4_SIZE=2048
ERASE_BLOCK_SIZE=4096

action_function ()
{
	nor_partition_dev_path="$1";
	action_name="$2";
	update_file="$3";
	block_num="$4";
	SECTOR_BLOCK_SIZE=4096;
	# echo "action for the commands: $nor_partition_dev_path, $action_name, $update_file, $block_num";
	if [ -c "$nor_partition_dev_path" ];
	then
	   case $action_name in
		"erase")
			echo "Starting to erase $nor_partition_dev_path";
			# echo "sudo flash_erase $nor_partition_dev_path 0 $block_num";
			sudo flash_erase $nor_partition_dev_path 0 $block_num >/dev/null 2>&1;
			echo "Complete erasing partition $nor_partition_dev_path zone";;
		"update")
			if [ -n "$update_file" ];
			then
				FIXED_SIZE=$((block_num*SECTOR_BLOCK_SIZE));
				# read input file into variable
				INPUT_SIZE=$(sudo wc -c < "$update_file");
				if [ $FIXED_SIZE -ge $INPUT_SIZE ]
				then
					echo "Starting to update $update_file to $nor_partition_dev_path of nor-flash";
					sudo flashcp -v $update_file $nor_partition_dev_path >/dev/null 2>&1
					# echo "Complete updating $update_file to partition $nor_partition_dev_path";
				else
					echo "The update file size: $INPUT_SIZE is larger than the current section size: $FIXED_SIZE"
					echo "The update file: $update_file Cannot be written."
				fi
			else
				echo "The written file is not input as the third parameter";
			fi;;
		"read")
			echo "Start to read nor-flash to $update_file"
			sudo dd if=$nor_partition_dev_path of=$update_file >/dev/null 2>&1;;
			# echo "Complete the reading partition $nor_partition_dev_path zone";;
		"compare")
			if [ -n "$update_file" ];
			then
				echo "Starting to compare $nor_partition_dev_path by using $update_file";
				sudo dd if=$nor_partition_dev_path of=/tmp/current_image.img >/dev/null 2>&1;
				file1="/tmp/current_image.img";
				# Fixed size file to be written
				file2="/tmp/generat_image.img";
				# determine the $nor_partition_dev_path data zone size
				FIXED_SIZE=$((block_num*SECTOR_BLOCK_SIZE));
				# read input file into variable
				INPUT_SIZE=$(sudo wc -c < "$update_file");
				# echo "The current update file size: $INPUT_SIZE, and fixed size: $FIXED_SIZE";
				# Read the contents of the input file into a variable
				# sudo dd if="$update_file" of=/dev/stdout bs=$fixed_size count=1 2>/dev/null | hexdump -v -e '1/1 "%.2x"'
				if [ $FIXED_SIZE -ge $INPUT_SIZE ]
				then
					sudo cp "$update_file" "$file2";
					sudo dd if=/dev/zero bs=1 count=$((FIXED_SIZE - INPUT_SIZE)) | tr "\000" "\377" >> "$file2";

					# Write the input file contents and filler characters to the output file
					#if diff "$file1" "$file2" >/dev/null ;
					if cmp -s "$file1" "$file2";
					then
						echo "The data in $nor_partition_dev_path zone is same as $update_file 's contents";
					else
						echo "The data in $nor_partition_dev_path zone is different from as $update_file 's contents";
					fi
					# echo "Complete comparing partition $nor_partition_dev_path zone by using $update_file";
				else
					echo "The update file size: $INPUT_SIZE is larger than the current section size: $FIXED_SIZE"
					echo "Cannot be compared for the current file."
				fi
			else
				echo "The verified file is not input as the third parameter";
			fi;;
		"update-verify")
			if [ -n "$update_file" ];
			then
				FIXED_SIZE=$((block_num*SECTOR_BLOCK_SIZE));
				# read input file into variable
				INPUT_SIZE=$(sudo wc -c < "$update_file");
				if [ $FIXED_SIZE -ge $INPUT_SIZE ]
				then
					echo "Starting to verify nor-flash at $nor_partition_dev_path by using $update_file";
					sudo flashcp -v $update_file $nor_partition_dev_path >/dev/null 2>&1
					# echo "Complete updating $update_file to partition $nor_partition_dev_path";
					sudo dd if=$nor_partition_dev_path of=/tmp/current_image.img >/dev/null 2>&1;
					file1="/tmp/current_image.img";
					# Fixed size file to be written
					file2="/tmp/generat_image.img";
					# determine the $nor_partition_dev_path data zone size
					FIXED_SIZE=$((block_num*SECTOR_BLOCK_SIZE));
					# read input file into variable
					INPUT_SIZE=$(sudo wc -c < "$update_file");
					sudo cp "$update_file" "$file2";
					sudo dd if=/dev/zero bs=1 count=$((FIXED_SIZE - INPUT_SIZE)) | tr "\000" "\377" >> "$file2";
					# Write the input file contents and filler characters to the output file
					#if diff "$file1" "$file2" >/dev/null ;
					if cmp -s "$file1" "$file2";
					then
						echo "The data in $nor_partition_dev_path zone is same as $update_file 's contents";
					else
						echo "The data in $nor_partition_dev_path zone is different from as $update_file 's contents";
					fi
					# echo "Complete update-verify partition $nor_partition_dev_path zone by using $update_file";
				else
					echo "The update file size: $INPUT_SIZE is larger than the current section size: $FIXED_SIZE"
					echo "The update file: $update_file Cannot be updated and verified."
				fi
			else
				echo "The updated file is not input as the third parameter";
			fi;;

		*) echo "Invalid action for partition $nor_partition_dev_path zone";;
	   esac;
	else
		echo "The partition does not exist.";
	fi
}
help_string="help"
version_string=$5
filename="/proc/device-tree/chip-version"
chip_version=""
#read chip_version < $filename
#echo "Reading device-tree chip-version: $chip_version"

if [ "$1" == "$help_string" ]; then
  echo "command line: sudo ./nor-flash {partition name} {erase|update|compare/update-verify} {file name} {block number} {type: A0/B0}"
else
    #if [ "$chip_version" == "$version_string" ];
    #then
    	case $partition in
		"mtd0" | "mtd1" | "mtd2" | "mtd3" | \
		"mtd4" )
			dev_file_path="/dev/$1";
            if [ -n "$3" ] && [ -n "$4" ];
			then
				action_function $dev_file_path $2 $3 $4;
	        else
				echo "Missing either update file or block size"
			fi;;	

		*)
			echo "Invalid partition or partition does not exist!!";;
   		esac
    #else
	#    echo "The input version is not matched device tree chip version: $version_string"
    #fi
fi
