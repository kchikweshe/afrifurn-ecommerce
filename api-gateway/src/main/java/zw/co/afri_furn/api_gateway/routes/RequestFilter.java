package zw.co.afri_furn.api_gateway.routes;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.cloud.gateway.filter.GatewayFilter;
import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;

import reactor.core.publisher.Mono;

@Component
public class RequestFilter implements GatewayFilter {
    private static final Logger logger = LoggerFactory.getLogger(RequestFilter.class);

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        Object body = exchange.getAttribute("cachedRequestBodyObject");
        logger.info("In request filter");
        logger.info("Body: {}", body);

        if (body == null) {
            logger.warn("Request body is null");
            // Handle the null body case if necessary
        }

        return chain.filter(exchange);
    }
}