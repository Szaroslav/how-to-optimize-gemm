filenames=(
  "MMult0"
  "MMult1"
  "MMult2"
  "MMult_1x4_3"
  "MMult_1x4_4"
  "MMult_1x4_5"
  "MMult_1x4_6"
  "MMult_1x4_7"
  "MMult_1x4_8"
  "MMult_1x4_9"
  "MMult_4x4_3"
  "MMult_4x4_4"
  "MMult_4x4_5"
  "MMult_4x4_6"
  "MMult_4x4_7"
  "MMult_4x4_8"
  "MMult_4x4_9"
  "MMult_4x4_10"
  "MMult_4x4_11"
  "MMult_4x4_12"
  "MMult_4x4_13"
  "MMult_4x4_14"
  "MMult_4x4_15"
)

for filename in "${filenames[@]}"; do
  make run NEW="$filename" OLD="$filename"
done
