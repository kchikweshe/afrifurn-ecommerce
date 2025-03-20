package zw.co.afri_furn.api_gateway.routes;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class Route {
        @Autowired
        RequestFilter requestFilter;

        @Bean
        public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
                String hostIp = "www.afri-furn.co.zw";
                String orderIP = "www.afri-furn.co.zw";

                return builder.routes()
                                .route("auth-service", r -> r.path("/auth")
                                                .uri("http://" + hostIp + ":8002/auth/api/v1/**"))
                                .route("product-service", r -> r.path("/product-service/api/v1/**")
                                                .uri("http://" + hostIp + ":8000/api/v1/**"))
                                .route("order-service", r -> r.path("/order")
                                                .uri("http://" + orderIP + ":8004/"))
                                .build();
        }
}
