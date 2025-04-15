# Use a Maven image with JDK 22 for the build stage
FROM maven:3.9.6-eclipse-temurin-21 AS build

# Set the working directory in the container
WORKDIR /app

# Copy the Maven wrapper and pom.xml to the container
COPY .mvn ./.mvn
COPY mvnw ./
COPY mvnw.cmd ./
COPY .gitignore ./
COPY pom.xml ./

# Copy the source code into the container
COPY src ./src

# Run the Maven build to package the application
RUN mvn clean package -DskipTests

# Use JDK 22 for the runtime stage
FROM eclipse-temurin:21-jdk-jammy

# Set the working directory for the runtime
WORKDIR /app

# Copy the packaged JAR file from the build stage
COPY --from=build /app/target/*.jar app.jar

# Command to run the application
CMD ["java", "-jar", "app.jar"]