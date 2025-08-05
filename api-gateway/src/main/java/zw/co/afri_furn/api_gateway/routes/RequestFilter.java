package zw.co.afri_furn.api_gateway.routes;

import java.util.function.Predicate;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.cloud.gateway.filter.GatewayFilter;
import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;

import com.google.common.net.HttpHeaders;

import reactor.core.publisher.Mono;

@Component
public class RequestFilter implements GatewayFilter {
    private static final Logger logger = LoggerFactory.getLogger(RequestFilter.class);
    Predicate<ServerWebExchange> isSecured = exchange -> {
        String authHeader = exchange.getRequest().getHeaders().getFirst(HttpHeaders.AUTHORIZATION);
        return authHeader != null && authHeader.startsWith("Bearer ");
    };

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        if (isSecured.test(exchange)) {
            logger.info("Auth header is null or does not start with Bearer");
            return chain.filter(exchange);
        }

        return chain.filter(exchange);
    }
}