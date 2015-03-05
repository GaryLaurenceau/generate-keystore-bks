# generate-keystore-bks
Generate keystore BKS file for Android to handle self signed HTTPS connection.

To generate BKS file you will need the Bouncy Castle jar file of your choice (maybe choose the last release).
You can find it [here](http://www.bouncycastle.org/latest_releases.html).
Get the public certificate of your server.

You can get it with this command:
```openssl s_client -showcerts -connect <SERVER_URL>:<SERVER_PORT> </dev/null```

And copy the root certificate in a file such as my_server.cer
(This command will be soon integrate in the generate.py script)

Now you can run generate.py in a terminal

``` ./generate.py -bc=<BOUNCY_CASTLE_FAR_LOCATION> --cacert=<CERTIFICATE_LOCATION> -p <PASSWORD>```

Choose a password between **6 and 8 characters**.
You can choose a password with more than 8 characters but it may cause problem with some version of Android

After getting the BKS file, you can put it in **/res/raw** directory and implement your HTTPClient

