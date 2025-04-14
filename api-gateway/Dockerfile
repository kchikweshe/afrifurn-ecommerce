# Use a Maven image with JDK 22 for the build stage
FROM maven:3.9.6-eclipse-temurin-22 AS build

WORKDIR /app

COPY .mvn ./.mvn
COPY mvnw ./
COPY pom.xml ./
ARG HOST_IP
ENV HOST_IP="afrifurn-product-service"
ARG EUREKA_HOST
ENV EUREKA_HOST="eureka-service"
COPY src ./src

RUN mvn clean package -DskipTests

# Use JDK 22 for the runtime stage
FROM eclipse-temurin:21-jdk-jammy

WORKDIR /app

COPY --from=build /app/target/*.jar app.jar

EXPOSE 8090

CMD ["java", "-jar", "app.jar"]