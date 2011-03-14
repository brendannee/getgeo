if [ -d "/Library/Python/2.6" ]; then
  mkdir /Library/Python/2.6/site-packages/getgeo
  cp * /Library/Python/2.6/site-packages/getgeo
else
  mkdir ~/.getgeo/getgeo
  cp * ~/.getgeo/getgeo
fi
cp getgeo /usr/bin
chmod +x /usr/bin/getgeo
