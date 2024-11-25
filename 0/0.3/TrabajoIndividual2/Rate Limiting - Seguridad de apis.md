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
- **APIs de terceros:** Servicios como AWS API Gateway o Azure API Management ofrecen configuraciones avanzadas de Rate Limiting.  

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

## **3. Integración del análisis de seguridad en el proyecto: módulo de foro**

### **3.1 Desafíos de seguridad en el módulo de foro**  
El módulo de foro enfrenta riesgos específicos que pueden comprometer la seguridad y la calidad del contenido. Entre los principales desafíos se encuentran:  

- **Contenido inapropiado o tóxico:** Publicaciones, comentarios y respuestas con lenguaje ofensivo, discriminatorio o violento.  
- **Ataques de spam:** Creación masiva de mensajes irrelevantes para saturar el sistema.  
- **Exposición a abuso de API:** Solicitudes excesivas o malintencionadas que pueden afectar la disponibilidad del servicio.  

### **3.2 Uso de Azure Content Safety**  
El servicio **Azure Content Safety** proporciona una API para analizar texto en busca de contenido inseguro o inadecuado. Este análisis se integra directamente en el flujo de moderación del módulo de foro, cubriendo publicaciones, comentarios y respuestas.

#### **3.2.1 Proceso de análisis**  
1. **Entrada:** Al crear o actualizar contenido (publicaciones, comentarios o respuestas), se envía el texto correspondiente al servicio Azure Content Safety.  
2. **Análisis:** La API evalúa el texto y devuelve un análisis de categorías inseguras, asignando una severidad a cada una.  
3. **Decisión:** Basándose en el resultado, el sistema permite o rechaza la acción:  
   - **Contenido seguro:** Se almacena en la base de datos.  
   - **Contenido inseguro:** Se informa al usuario del rechazo y las razones asociadas.  

#### **3.2.2 Ejemplo de implementación**  
**Lógica de moderación reutilizable:**  

```typescript
async function analyzeContentSafety(
  title: string,
  content: string,
  tags: string[],
): Promise<{ isSafe: boolean; unsafeCategories?: string }> {
  const textToAnalyze = [title, content, ...tags].join('\n---\n');
  const analysisResult = await this.contentSafetyService.analyzeText(textToAnalyze);

  if (!analysisResult.isSafe) {
    const unsafeCategories = analysisResult.unsafeCategories
      .map((cat) => `${cat.category} (Severidad: ${cat.severity})`)
      .join(', ');
    return { isSafe: false, unsafeCategories };
  }

  return { isSafe: true };
}
```

## **4. Análisis del patrón Rate Limiting en el módulo de foro**

### **4.1 Importancia del Rate Limiting en el módulo de foro**  
En el módulo de foro, donde los usuarios pueden crear publicaciones, comentarios y respuestas de manera continua, es esencial implementar mecanismos para evitar abusos y garantizar el acceso equitativo a los recursos. Sin un control adecuado, podrían presentarse problemas como:

- **Sobrecarga del sistema:** Solicitudes masivas o continuas que ralentizan la experiencia de otros usuarios.  
- **Consumo excesivo de recursos de terceros:** Como la API de Azure Content Safety, que tiene un costo asociado por cada análisis realizado.  
- **Vulnerabilidad frente a ataques:** Ataques como fuerza bruta o denegación de servicio podrían comprometer la estabilidad del sistema.  

El patrón **Rate Limiting** mitiga estos riesgos al establecer límites en la cantidad de solicitudes permitidas para cada usuario en un período determinado. Esto permite proteger los recursos y mantener un entorno funcional para todos.

### **4.2 Implementación del Rate Limiting en el módulo de foro**

#### **4.2.1 Selección de la estrategia**  
Existen diferentes estrategias para implementar Rate Limiting. En este caso, se utiliza la estrategia de **Token Bucket** (cubo de fichas), que permite acumular solicitudes hasta cierto límite y las procesa gradualmente:  

- Cada usuario tiene un "cubo" que acumula fichas (tokens).  
- Cada solicitud consume una ficha.  
- Las fichas se regeneran con el tiempo, según un intervalo predefinido.  

#### **4.2.2 Integración en el proyecto**  
En el proyecto, el **Rate Limiting** se configura usando un middleware que limita las solicitudes por endpoint. Para ello, se utiliza el paquete `nestjs-throttler`.

**Instalación:**  
```bash
npm install @nestjs/throttler
```

## **5. Práctica aplicada: Implementación de análisis de seguridad y Rate Limiting en el módulo de foro**

### **5.1 Introducción**  
En esta sección, se detallan los pasos prácticos que se siguieron para integrar el análisis de seguridad con Azure Content Safety y el patrón Rate Limiting en el módulo de foro del proyecto. Esta integración asegura que el sistema sea tanto seguro como eficiente en el manejo de contenido generado por los usuarios.

### **5.2 Integración de Azure Content Safety en el módulo de foro**  

#### **5.2.1 Configuración inicial**  
Para integrar Azure Content Safety, se configuraron las claves de acceso y el endpoint del servicio en un archivo `.env`, siguiendo las mejores prácticas de seguridad:  
```env
AZURE_API_KEY=TU_API_KEY_AQUI
AZURE_ENDPOINT=TU_ENDPOINT_AQUI
```