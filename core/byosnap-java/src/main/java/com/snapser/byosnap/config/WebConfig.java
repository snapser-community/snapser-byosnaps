package com.snapser.byosnap.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import com.snapser.byosnap.auth.AuthorizationInterceptor;

/**
 * Wires up the authorization interceptor and CORS.
 *
 * <p>CORS is enabled because the Snapser API Explorer runs in the browser —
 * enabling CORS lets you exercise the APIs from the API Explorer. We allow all
 * origins and methods, and the headers Snapser uses.
 */
@Configuration
public class WebConfig implements WebMvcConfigurer {

    private final AuthorizationInterceptor authorizationInterceptor;

    @Autowired
    public WebConfig(AuthorizationInterceptor authorizationInterceptor) {
        this.authorizationInterceptor = authorizationInterceptor;
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // The interceptor is a no-op unless the handler carries @ValidateAuthorization,
        // so it is safe to register it against every path.
        registry.addInterceptor(authorizationInterceptor).addPathPatterns("/**");
    }

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        // @GOTCHAS - CORS
        //   1. The Snapser API Explorer runs in the browser. Enabling CORS lets
        //      you access the APIs via the API Explorer.
        registry.addMapping("/**")
                .allowedOriginPatterns("*")
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH")
                .allowedHeaders("Content-Type", "Token", "Api-Key", "App-Key", "Gateway", "User-Id");
    }
}
