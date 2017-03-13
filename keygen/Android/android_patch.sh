# Generate .a files

python elf_patch.py --aes-enc ../certificate/aes_decrypt_key --aes-dec ../certificate/aes_encrypt_key --rsa-private ../certificate/rsa_client_pri.der --rsa-public ../certificate/rsa_server_pri.der ../original/android/armeabi/libiqiyi_temp.a ../../android/native/jni/armeabi/libiqiyi_temp.a

python elf_patch.py --aes-enc ../certificate/aes_decrypt_key --aes-dec ../certificate/aes_encrypt_key --rsa-private ../certificate/rsa_client_pri.der --rsa-public ../certificate/rsa_server_pri.der ../original/android/armeabi-v7a/libiqiyi_temp.a ../../android/native/jni/armeabi-v7a/libiqiyi_temp.a

# Build .so files

cd ../../android/native/jni

ndk-build clean

ndk-build

# Return to original dir

cd -

# Clear output

rm -rf ../output/android

mkdir ../output/android

# Copy patched android libs

cp -r ../../android/native/libs ../output/android/
