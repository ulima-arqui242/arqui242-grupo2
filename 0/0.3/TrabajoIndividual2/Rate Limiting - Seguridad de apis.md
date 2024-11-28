# **Análisis de Seguridad de APIs e Implementación del Patrón Rate Limiting**

## **1. Introducción**

### **1.1 ¿Qué es la seguridad en APIs?**  
Las **APIs (Interfaces de Programación de Aplicaciones)** son un componente fundamental en el desarrollo de software moderno, ya que permiten la comunicación y el intercambio de datos entre diferentes sistemas, servicios o aplicaciones. Dado que muchas aplicaciones dependen de las APIs para interactuar con bases de datos, servicios externos y usuarios, garantizar su **seguridad** es esencial para proteger los datos, la infraestructura y la experiencia del usuario.

La seguridad en APIs se refiere a un conjunto de prácticas, configuraciones y patrones de diseño destinados a mitigar riesgos y proteger las APIs contra accesos no autorizados, abuso de recursos y otras amenazas. Una API segura asegura que solo usuarios y sistemas autorizados puedan acceder y utilizar los servicios ofrecidos, evitando así posibles vulnerabilidades que puedan comprometer el sistema.  

### **1.2 Riesgos y amenazas comunes**  
Las APIs son un objetivo común para los atacantes debido a su naturaleza expuesta. Entre los riesgos más frecuentes, se encuentran:  

- **Ataques de Denegación de Servicio (DoS/DDoS):**  
  Los atacantes generan un alto volumen de solicitudes para saturar la API y dejarla fuera de servicio.  

- **Abuso de recursos:**  
  Usuarios legítimos o no autorizados realizan un número excesivo de llamadas a la API, afectando el rendimiento del sistema o generando costos innecesarios.  

- **Explotación de endpoints vulnerables:**  
  Los endpoints mal configurados o expuestos sin restricciones adecuadas pueden permitir accesos no deseados, divulgación de datos sensibles o la manipulación del sistema.  

- **Inyección de código o datos maliciosos:**  
  Amenazas como ataques de inyección SQL, cross-site scripting (XSS) o inyecciones de comandos afectan la integridad y seguridad del sistema.  

Por estas razones, es fundamental diseñar y configurar APIs con un enfoque centrado en la seguridad.  

### **1.3 Objetivo del informe**  
Este informe tiene como propósito analizar los aspectos clave de la seguridad en APIs, con un enfoque especial en la implementación del patrón de diseño **Rate Limiting**, una estrategia ampliamente utilizada para mitigar riesgos relacionados con el abuso de recursos y los ataques de denegación de servicio.  

Además, se presentará una aplicación práctica de este patrón en el **módulo de foro de discusión** del proyecto del curso, donde se abordarán aspectos como:  
1. La protección contra la creación excesiva de publicaciones y comentarios.  
2. La configuración de límites de solicitudes a nivel global y específico. 

En última instancia, este informe busca proporcionar una guía práctica y teórica para entender y aplicar medidas de seguridad en APIs modernas.  

## **2. Análisis de seguridad de APIs y el patrón Rate Limiting**

### **2.1 El rol de la seguridad en APIs**  
La seguridad en las APIs no solo protege los datos sensibles y la infraestructura, sino que también garantiza la calidad del servicio para los verdaderos usuarios. Un diseño robusto incluye autenticación, autorización, cifrado, validación de entradas y mecanismos para prevenir abusos. Sin embargo, la **prevención de abusos de recursos** es uno de los desafíos más críticos en aplicaciones modernas, especialmente en sistemas expuestos públicamente o que operan en la nube.  

### **2.2 ¿Qué es el patrón Rate Limiting?**  
El patrón **Rate Limiting** es una estrategia que controla la cantidad de solicitudes que un cliente (usuario, sistema o IP) puede hacer a una API dentro de un intervalo de tiempo. Este patrón es esencial para mitigar los siguientes riesgos:  

- **Prevención de abusos:** Evita que un cliente sobrecargue la API con un número excesivo de solicitudes.  
- **Mitigación de ataques DDoS:** Reduce el impacto de solicitudes maliciosas al limitar la capacidad de un atacante para saturar el sistema.  
- **Control de costos:** En entornos de nube, un uso descontrolado puede generar costos innecesarios al consumir recursos computacionales o de red.  
- **Garantía de equidad:** Asegura que los recursos de la API estén disponibles equitativamente para todos los usuarios.  

El objetivo de este patrón es proteger la infraestructura subyacente mientras se mantiene la calidad del servicio para usuarios legítimos.

### **2.3 Tipos de Rate Limiting**  
Existen varias implementaciones de Rate Limiting, dependiendo del caso de uso:  

#### **2.3.1 Fixed Window (Ventana fija):**  
Se define un límite de solicitudes por cliente dentro de una ventana de tiempo específica, como 100 solicitudes por minuto. Este método es fácil de implementar, pero puede ser susceptible a picos de tráfico al inicio de cada ventana.  

#### **2.3.2 Sliding Window (Ventana deslizante):**  
Similar al modelo de ventana fija, pero en este caso, el límite se evalúa dinámicamente sobre un intervalo de tiempo continuo. Esto reduce la susceptibilidad a picos de tráfico.  

#### **2.3.3 Token Bucket (Cubo de fichas):**  
Este enfoque utiliza un "cubo" con un número limitado de fichas que representa la capacidad de solicitudes permitidas. Los clientes consumen una ficha por solicitud, y las fichas se recargan a una tasa constante. Este modelo permite ráfagas de tráfico controladas mientras mantiene un límite promedio.  

#### **2.3.4 Leaky Bucket (Cubo con fugas):**  
En este modelo, las solicitudes se agregan a un "cubo", pero las solicitudes se procesan a una tasa fija. Si el cubo se llena, las solicitudes adicionales se descartan o rechazan.  

### **2.4 Implementación técnica del patrón Rate Limiting**  

#### **2.4.1 Herramientas comunes para Rate Limiting**  
- **Bibliotecas y middleware:** Frameworks como Express.js en Node.js o NestJS ofrecen soluciones integradas para aplicar Rate Limiting.  
- **Almacenamiento de estado:** Para implementar límites distribuidos, se utilizan soluciones como Redis o bases de datos en memoria para almacenar los contadores de solicitudes.  

#### **2.4.2 Configuración básica en NestJS**  
NestJS permite la integración del middleware `express-rate-limit` para limitar las solicitudes de forma sencilla:  

```typescript
import * as rateLimit from 'express-rate-limit';
import { Module, MiddlewareConsumer, NestModule } from '@nestjs/common';

@Module({
  imports: [],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer
      .apply(
        rateLimit({
          windowMs: 1 * 60 * 1000, // 1 minuto
          max: 100, // Máximo de 100 solicitudes por minuto
        }),
      )
      .forRoutes('*');
  }
}
```

Pero tambien permite el uso de este patron usando dependencias nativas de NestJs como `nestjs-throttler`. Para el caso practico se usará este último.

## **3. Integración del análisis de seguridad en el proyecto: módulo de foro**

### **3.1 Desafíos de seguridad en el módulo de foro**  
El módulo de foro enfrenta riesgos específicos que pueden comprometer la seguridad y la calidad del contenido. Entre los principales desafíos se encuentran:  

- **Contenido inapropiado o tóxico:** Publicaciones, comentarios y respuestas con lenguaje ofensivo, discriminatorio o violento.  
- **Ataques de spam:** Creación masiva de mensajes irrelevantes para saturar el sistema.  
- **Exposición a abuso de API:** Solicitudes excesivas o malintencionadas que pueden afectar la disponibilidad del servicio.  

## **4. Análisis del patrón Rate Limiting en el módulo de foro**

### **4.1 Importancia del Rate Limiting en el módulo de foro**  
En el módulo de foro, donde los usuarios pueden crear publicaciones, comentarios y respuestas de manera continua, es esencial implementar mecanismos para evitar abusos y garantizar el acceso equitativo a los recursos. Sin un control adecuado, podrían presentarse problemas como:

- **Sobrecarga del sistema:** Solicitudes masivas o continuas que ralentizan la experiencia de otros usuarios.  
- **Consumo excesivo de recursos de terceros:** Como la API de Azure Content Safety, que tiene un costo asociado por cada análisis realizado.  
- **Vulnerabilidad frente a ataques:** Ataques como fuerza bruta o denegación de servicio podrían comprometer la estabilidad del sistema.  

El patrón **Rate Limiting** mitiga estos riesgos al establecer límites en la cantidad de solicitudes permitidas para cada usuario en un período determinado. Esto permite proteger los recursos y mantener un entorno funcional para todos.

### **4.2 Implementación del Rate Limiting en el módulo de foro**

#### **4.2.1 Selección de la estrategia**  
Existen diversas estrategias para implementar *Rate Limiting*. En este caso, se adopta la estrategia de **Fixed Window** (ventana fija), que permite establecer un límite máximo de solicitudes por usuario dentro de un intervalo de tiempo predefinido. Esta estrategia opera de la siguiente manera:  

- **Límite fijo por ventana**: Cada usuario tiene un límite de solicitudes que puede realizar durante una ventana de tiempo específica (por ejemplo, 100 solicitudes por minuto).  
- **Reinicio al final de la ventana**: El contador de solicitudes se reinicia al comienzo de cada nueva ventana de tiempo, independientemente de las solicitudes restantes del usuario en la ventana anterior.  
- **Procesamiento inmediato**: Las solicitudes se procesan inmediatamente siempre que el usuario no haya excedido el límite asignado.  
- **Bloqueo temporal**: Si el límite se supera antes de que termine la ventana, las solicitudes adicionales se rechazan hasta que comience la siguiente ventana.  

Esta estrategia es adecuada para casos en los que el límite de solicitudes puede ser estrictamente delimitado en periodos regulares, aunque puede presentar inconsistencias si las solicitudes ocurren cerca del límite de la ventana (por ejemplo, al final de una y al inicio de la siguiente).  

#### **4.2.2 Integración en el proyecto**  
En el proyecto, el **Rate Limiting** se configura usando un middleware que limita las solicitudes por endpoint. Para ello, se utiliza el paquete `nestjs-throttler`.

**Instalación:**  
```bash
npm install @nestjs/throttler
```

## **5. Práctica aplicada: Implementación de análisis de seguridad y Rate Limiting en el módulo de foro**

### **5.1 Introducción**  
En esta sección, se detallan los pasos prácticos que se siguieron para integrar el patrón Rate Limiting para proteger un el método `getAllPosts()` del controlador en el módulo de foro del proyecto. Esta integración asegura que el sistema restringa el uso desmedido de un servicio en particular, para este caso se usó ese para facilitar la comprensión.

### **5.2 Configuración en el módulo de foro**  

#### **5.2.1 Configuración inicial**  
Para poder usar uso de `nestjs-throttler` en el proyecto primero se debe configurarlo en el `app.module.ts` del proyecto. De la siguiente manera: 

```js
import { Module } from '@nestjs/common';
import { ThrottlerModule } from '@nestjs/throttler';

@Module({
  imports: [
    // resto del código 
    ThrottlerModule.forRoot({
      throttlers: [
        {
          ttl: 60 * 1000, // Tiempo de vida en milisegundos
          limit: 10, // Número máximo de solicitudes permitidas por minuto
        },
      ],
    }),
  ],
})
export class AppModule {}
```

#### **5.2.2 Creación de un guard personalizado**  
En nestJs te permite crear tus propias salidas personalizadas cuando un servicio de tu controlador responda con los limites que definiste anteriormente. Para ello, haremos uso del comando de CLI de nestJs para crear uno automáticamente

```bash
nest g gu custom --no-spec
```

usamos `--no-spec` para no crear el archivo test. Eso crearia el archivo `custom.guards.ts` en una carpeta llamada `custom`. Para el caso del modulo del foro se tiene lo siguiente.

```js
import { Injectable, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { ThrottlerGuard, ThrottlerException, ThrottlerStorageService, ThrottlerModuleOptions } from '@nestjs/throttler';

@Injectable()
export class CustomThrottlerGuard extends ThrottlerGuard {
  constructor(
    protected readonly options: ThrottlerModuleOptions,
    protected readonly throttlerStorage: ThrottlerStorageService,
    protected readonly reflector: Reflector,
  ) {
    super(options, throttlerStorage, reflector);
  }

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const canActivate = await super.canActivate(context);
    if (!canActivate) {
      this.throwThrottlingException(context);
    }
    return canActivate;
  }

  protected async throwThrottlingException(context: ExecutionContext): Promise<void> {
    throw new ThrottlerException('Too many requests, please try again later.');
  }
}
```

Aquí se configuró un guard personalizado para que cuando se incumpla una regla en un método en nuestro controlador muestre este mensaje personalizado `Too many requests, please try again later`.

#### **5.2.3 Configurando nuestro guard personalizado**
Para poder usar lo anterior se debe configurar en el `app.module.ts` de tu proyecto. Para mi caso se haría de la siguiente manera.

```js
import { Module } from '@nestjs/common';
import { ThrottlerModule } from '@nestjs/throttler';
import { APP_GUARD } from '@nestjs/core';
import { CustomThrottlerGuard } from './forum/guards/custom-throttler.guard';

@Module({
  imports: [
    // resto del código 
    ThrottlerModule.forRoot({
      throttlers: [
        {
          ttl: 60 * 1000,
          limit: 10, 
        },
      ],
    }),
  ],
  providers: [
    {
      provide: APP_GUARD,
      useClass: CustomThrottlerGuard,
    },
  ],
})
export class AppModule {}
```

En imports, agregas la propiedad `providers`, usas un arreglo y dentro de él creas un objeto con dos propiedades en `provide` le asignas el `APP_GUARD` del modulo de `@nestjs/core` y en `useClass` asignas tu guard customizado.

#### 5.2.2 Aplicando la regla a un controlador
Ahora le agregaremos la regla a un metodo de nuestro controlador usando `@Throttle`.

```js
// 2. Obtener todos los posts
  @Get()
  @Throttle({ default: { limit: 3, ttl: 60000 } })
  async getAllPosts() {
    return this.postService.getAllPosts();
  }
```
Aquí se puso la regla que cuando este metodo se llame 3 veces en un cuadro de tiempo de 60 segundos, lanzará el guard custom que configuramos anteriormente y no se podrá usar ese método hasta que se cumpla el tiempo establecido en la regla. Con esto podrás proteger tus servicios.


### 6. Anexos

  - Enlace del vídeo: https://youtu.be/H6pftHKOP7s
  - Enlace del repositorio: https://github.com/Joselinares17/respawn-chatter-backend/tree/jose

### 7. Referencias

  - Asaolu, E. (2024, 22 julio). Rate limiting vs. throttling and other API traffic management - LogRocket Blog. LogRocket Blog. https://blog.logrocket.com/advanced-guide-rate-limiting-api-traffic-management/
  - Documentation | NestJS - A progressive Node.js framework. (s. f.). Documentation | NestJS - A Progressive Node.js Framework. https://docs.nestjs.com/security/rate-limiting
  - Mohsen, F. (2023, 23 abril). Rate limiting using throttler in nest JS - Fadi Mohsen - Medium. Medium. https://medium.com/@Xfade/rate-limiting-using-throttler-in-nest-js-fb74b6661050
  - Patange, A. (2024, 21 junio). System Design (HLD+LLD): I built a Dynamic Rate-Limiter in NestJS. Here’s What I Learnt! https://www.linkedin.com/pulse/system-design-hldlld-i-built-dynamic-rate-limiter-nestjs-patange-wrdyf/
