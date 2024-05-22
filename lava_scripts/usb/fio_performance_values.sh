#!/bin/bash
#set -x
# this script requires fio bc & jc

umount /dev/sd*
sync
# Directory to test
TEST_DIR=$1

# Parameters for the tests should be representive of the workload you want to simulate
BS="4k"             # Block size
IOENGINE="libaio"   # IO engine
IODEPTH="16"        # IO depth sets how many I/O requests a single job can handle at once
DIRECT="1"          # Direct IO at 0 is buffered with RAM which may skew results and I/O 1 is unbuffered
NUMJOBS="18"         # Number of jobs is how many independent I/O streams are being sent to the storage
FSYNC="0"           # Fsync 0 leaves flushing up to Linux 1 force write commits to disk
NUMFILES="1"        # Number of files is number of independent I/O threads or processes that FIO will spawn
FILESIZE="200M"       # File size for the tests, you can use: K M G
RUNTIME=240


# Function to perform FIO test and display average output
perform_test() {
    RW_TYPE=$1
    TEST_FILE=$2


    echo "#######  $RW_TYPE performance values ##########"
    #echo "Running $RW_TYPE test with block size $BS, ioengine $IOENGINE, iodepth $IODEPTH, direct $DIRECT, numjobs $NUMJOBS, fsync $FSYNC, using $NUMFILES files of size $FILESIZE on $TEST_DIR"
    echo "Running $RW_TYPE test with block size $BS, iodepth $IODEPTH, direct $DIRECT, numjobs $NUMJOBS, fsync $FSYNC, using $NUMFILES files of size $FILESIZE on $TEST_FILE"

    # Initialize variables to store cumulative values
    TOTAL_READ_IOPS=0
    TOTAL_WRITE_IOPS=0
    TOTAL_READ_BW=0
    TOTAL_WRITE_BW=0

    for ((i=1; i<=NUMFILES; i++)); do
        #TEST_FILE="$TEST_DIR/fio_test_file_$i"
	#TEST_FILE="/dev/sda1"

        # Running FIO for each file and parsing output
	set -x
          echo "fio arguments fio --name=$RW_TYPE  --filename=$TEST_FILE --rw=$RW_TYPE --bs=$BS   --iodepth=$IODEPTH --direct=$DIRECT  --numjobs=$NUMJOBS --size=$FILESIZE  --group_reporting --runtime=$RUNTIME --allow_mounted_write=1 --output-format=json" 
	set +x
          OUTPUT=$(fio --name=$RW_TYPE  \
                             --filename=$TEST_FILE --rw=$RW_TYPE \
                             --bs=$BS  \
                             --iodepth=$IODEPTH \
                             --direct=$DIRECT \
                             --numjobs=$NUMJOBS \
                             --size=$FILESIZE \
                             --group_reporting \
                             --runtime=$RUNTIME \
                             --allow_mounted_write=1 \
                             --output-format=json )
        # OUTPUT=$(fio --name=test_$i \
                     # --filename=$TEST_FILE \
                     # --rw=$RW_TYPE \
                     # --bs=$BS \
                     # --ioengine=$IOENGINE \
                     # --iodepth=$IODEPTH \
                     # --direct=$DIRECT \
                     # --numjobs=$NUMJOBS \
                     # --fsync=$FSYNC \
                     # --size=$FILESIZE \
                     # --group_reporting \
                     # --output-format=json)

        # Accumulate values
        TOTAL_READ_IOPS=$(echo $OUTPUT | jq '.jobs[0].read.iops + '"$TOTAL_READ_IOPS")
        TOTAL_WRITE_IOPS=$(echo $OUTPUT | jq '.jobs[0].write.iops + '"$TOTAL_WRITE_IOPS")
        TOTAL_READ_BW=$(echo $OUTPUT | jq '(.jobs[0].read.bw / 1024) + '"$TOTAL_READ_BW")
        TOTAL_WRITE_BW=$(echo $OUTPUT | jq '(.jobs[0].write.bw / 1024) + '"$TOTAL_WRITE_BW")
    done

   # Calculate averages
    AVG_READ_IOPS=$(echo "$TOTAL_READ_IOPS / $NUMFILES" | bc -l)
    AVG_WRITE_IOPS=$(echo "$TOTAL_WRITE_IOPS / $NUMFILES" | bc -l)
    AVG_READ_BW=$(echo "$TOTAL_READ_BW / $NUMFILES" | bc -l)
    AVG_WRITE_BW=$(echo "$TOTAL_WRITE_BW / $NUMFILES" | bc -l)

    # Format and print averages, omitting 0 results
    [ "$(echo "$AVG_READ_IOPS > 0" | bc)" -eq 1 ] && printf "$RW_TYPE : Average Read IOPS: %'.2f\n" $AVG_READ_IOPS
    [ "$(echo "$AVG_WRITE_IOPS > 0" | bc)" -eq 1 ] && printf "$RW_TYPE : Average Write IOPS: %'.2f\n" $AVG_WRITE_IOPS
    [ "$(echo "$AVG_READ_BW > 0" | bc)" -eq 1 ] && printf "$RW_TYPE : Average Read Bandwidth (MB/s): %'.2f\n" $AVG_READ_BW
    [ "$(echo "$AVG_WRITE_BW > 0" | bc)" -eq 1 ] && printf "$RW_TYPE : Average Write Bandwidth (MB/s): %'.2f\n" $AVG_WRITE_BW
    echo "#######  $RW_TYPE performance values ##########"

}

# Run tests
perform_test write "/dev/sda1"
perform_test read "/dev/sda1"
perform_test randwrite "/dev/sda1"
perform_test randread "/dev/sda1"
##perform_test readwrite "/dev/sda1"

# # Clean up
# for ((i=1; i<=NUMFILES; i++)); do
    # rm "$TEST_DIR/fio_test_file_$i"
# done
