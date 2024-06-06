# Use an official Node.js runtime as a parent image
FROM node:22


# Set the working directory in the container to /app
WORKDIR /app

# TODO: this is an hugly workaround...
RUN chown 1010:1010 /app
RUN mkdir /.npm
RUN chown -R 1010:1010 /.npm
USER 1010:1010

# Copy the current directory contents into the container at /app
#COPY . /app

# Install any needed packages specified in package.json
#RUN npm install

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run the app when the container launches
#CMD ["npm", "start"]