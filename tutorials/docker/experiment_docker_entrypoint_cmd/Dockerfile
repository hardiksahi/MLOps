# ## Only entrypoint
# FROM alpine:latest
# ENTRYPOINT ["ls"]

# ## Only cmd
# FROM alpine:latest
# CMD ["ls"]

## Both entrypoint and cmd
# FROM alpine:latest
# ENTRYPOINT ["ls"]
# CMD ["-alh"]



#############################

# ## Only entrypoint
FROM ubuntu:20.04
RUN <<EOF
apt-get update;
apt-get install -y apache2-utils;
rm -rf /var/lib/apt/lists/*;
EOF
ENTRYPOINT ["ab"]

# ## Only cmd
# FROM ubuntu:20.04
# RUN <<EOF
# apt-get update;
# apt-get install -y apache2-utils;
# rm -rf /var/lib/apt/lists/*;
# EOF
# CMD ["ab"]