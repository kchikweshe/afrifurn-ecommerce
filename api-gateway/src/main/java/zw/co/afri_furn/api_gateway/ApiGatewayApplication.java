package zw.co.afri_furn.api_gateway;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@SpringBootApplication
@EnableDiscoveryClient
public class ApiGatewayApplication {

	public static void main(String[] args) {
		String hostIp = System.getenv().get("HOST_IP");
		String eureka = System.getenv().get("EUREKA HOST");

		System.err.println("Host ip============"+hostIp);
		System.err.println("EUREKA HOST============"+eureka);

		SpringApplication.run(ApiGatewayApplication.class, args);
	}

}
