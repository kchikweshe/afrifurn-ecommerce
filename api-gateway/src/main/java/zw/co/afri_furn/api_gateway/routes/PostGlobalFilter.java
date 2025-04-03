package zw.co.afri_furn.api_gateway.routes;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.reactivestreams.Publisher;
import org.springframework.core.io.buffer.DataBuffer;
import org.springframework.core.io.buffer.DataBufferFactory;
import org.springframework.core.io.buffer.DefaultDataBuffer;
import org.springframework.core.io.buffer.DefaultDataBufferFactory;
import org.springframework.http.server.reactive.ServerHttpRequest;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.http.server.reactive.ServerHttpResponseDecorator;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import org.springframework.web.server.WebFilter;
import org.springframework.web.server.WebFilterChain;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.nio.charset.StandardCharsets;
import java.util.List;
@Component
public class PostGlobalFilter implements WebFilter {

    @Override
    public Mono<Void> filter(@SuppressWarnings("null") ServerWebExchange exchange, @SuppressWarnings("null") WebFilterChain chain) {
        String path = exchange.getRequest().getPath().toString();
        ServerHttpResponse response = exchange.getResponse();
        ServerHttpRequest request = exchange.getRequest();
        DataBufferFactory dataBufferFactory = response.bufferFactory();
        ServerHttpResponseDecorator decoratedResponse = getDecoratedResponse(path, response, request, dataBufferFactory);
        return chain.filter(exchange.mutate().response(decoratedResponse).build());
    }

    private ServerHttpResponseDecorator getDecoratedResponse(String path, ServerHttpResponse response, ServerHttpRequest request, DataBufferFactory dataBufferFactory) {
        return new ServerHttpResponseDecorator(response) {

            @Override 
            public Mono<Void> writeWith(final Publisher<? extends DataBuffer> body) {

                if (body instanceof Flux) {

                    Flux<? extends DataBuffer> fluxBody = (Flux<? extends DataBuffer>) body;

                    return super.writeWith(fluxBody.buffer().map(dataBuffers -> {

                        DefaultDataBuffer joinedBuffers = new DefaultDataBufferFactory().join(dataBuffers);
                        byte[] content = new byte[joinedBuffers.readableByteCount()];
                        joinedBuffers.read(content);
                        String responseBody = new String(content, StandardCharsets.UTF_8);//MODIFY RESPONSE and Return the Modified response
                        System.out.println("RequestId:\n"+request.getId()+",\n method: "+request.getMethod()+",\n Req URL: "+request.getURI()+", \n Response Body :\n"+ responseBody);
                        try {
                            if(request.getURI().getPath().equals("/auth") && request.getMethod().equals("GET")) {
                                List<Object> student = new ObjectMapper().readValue(responseBody, List.class);
                                System.out.println("student:" + student);
                            }
                            else if(request.getURI().getPath().equals("/second") && request.getMethod().equals("GET")) {
                                List<Object> companies = new ObjectMapper().readValue(responseBody, List.class);
                                System.out.println("companies:" + companies);
                            }
                        } catch (JsonProcessingException e) {
                            throw new RuntimeException(e);
                        }
                        return dataBufferFactory.wrap(responseBody.getBytes());
                    })).onErrorResume(err -> {

                        System.out.println("error while decorating Response: {}"+err.getMessage());
                        return Mono.empty();
                    });

                }
                return super.writeWith(body);
            }
        };
    }

}