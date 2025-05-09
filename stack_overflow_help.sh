python3 volatilefs.py
printf "\n\n"
echo "Normal Database managed by sqlite: "
echo "------------------------------------------------------------------------------"
printf "\n\n"
hexdump -C test_sqlite
printf "\n\n"
echo "The buffer that come from my VFS with exact same commands executed on it: "
echo "------------------------------------------------------------------------------"
printf "\n\n"
hexdump -C buffer3
