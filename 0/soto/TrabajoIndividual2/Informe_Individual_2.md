
# Jean Pierre Soto Tipacti - Retry Pattern

1. **Desarrollo del Patrón**:
  
   - **Problema**
Una aplicación que se conecta con componentes cloud se espera que sea capaz de manejar o sobrellevar fallas transitorias que puedan ocurrir en este tipo de entornos, algunos de estas fallas pueden ser pequeñas interrupciones o pérdida temporal de conectividad a la red, una indisponibilidad del servicio o tiempos de espera que ocurren cuando un servicio se encuentra ocupado (usualmente, se da en servicios muy demandados que reciben múltiples solicitudes). Estas fallas típicamente se autocorrigen después de un tiempo, lo que lleva a que sea apropiado realizar una repetición del mismo llamado, por ejemplo, una base de datos que recibe múltiples solicitudes concurrentemente puede no responder a alguna, pero es factible que responda de realizar un nuevo intento después de un tiempo. Entonces, en resumen, se tiene un problema existente en posibles fallos temporales en algunos servicios que la aplicación requiere para su funcionamiento y que requieren de una solución.
  
   - **Solución**
El patrón Retry ofrece tres estrategias de solución, las cuales pueden ser aplicadas dependiendo del contexto de la aplicación, las estrategias son las siguientes:

		- Cancelar: Esta estrategia es recomendada cuando no se trata de un error transitorio y se encuentra poco probable que haya éxito en una repetición, en este caso se debería de cancelar la operación y enviar una excepción, por ejemplo, cuando busca realizar una autenticación y se tienen credenciales inválidas, por mucho que se reintente no se logrará tener éxito en la operación.
		
		- Reintentar: Esta estrategia se recomienda cuando la falla ocurre por una razón rara o inusual, podría haberse originado por circunstancias inusuales como una corrupción del paquete de red durante la transmisión, en este caso, se podría enviar la solicitud fallida nuevamente inmediatamente, puesto que se estima como poco probable que el error o falla vuelva a ocurrir, por lo que es muy factible que se tenga éxito.
		
		- Reintentar después de un retraso: Si la falla ocurrida es una de las fallas de conectividad o de ocupación más comunes, la red o el propio servicio podrían necesitar algo de tiempo mientras corrigen los problemas de conectividad o de ocupación. La aplicación debería esperar un tiempo antes de volver a enviar la solicitud, para las fallas más comunes se recomienda que se tenga estimado un periodo de tiempo entre reintentos para poder distribuir las solicitudes lo más uniformemente posible. Esto se realiza debido a que es más probable que el servicio se haya podido liberar de la sobrecarga, si reintentamos muy rápido y enviamos muchas solicitudes, no permitiremos que el servicio pueda liberarse de la sobrecarga. También se recomienda que  para esta estrategia se tenga un número de intentos limitados para que no se espere una respuesta eternamente ni se realicen reintentos infinitos. Por último, se debe considerar la existencia de un incremento exponencial entre los reintentos, pues no todas las fallas son iguales y podría existir alguna que necesito un poco más de tiempo, así que entre intento e intento sería conveniente que se apliquen periodos de tiempo que se vayan incrementando, por ejemplo entre el intento 1 y 2 se podría tener un tiempo de 2 segundos, y entre el intento 2 y 3 se podría tener un tiempo de 4 segundos.

   - **Casos de Aplicación**:
		#### 1. **E-commerce y Procesamiento de Pagos**
		
		-   **Escenario**: Una plataforma de comercio electrónico necesita realizar múltiples transacciones diarias a través de procesadores de pago externos, como Stripe o PayPal.
		-   **Uso del Patrón**: Cuando el sistema intenta procesar pagos, puede encontrar errores temporales debido a problemas de red, latencia o sobrecarga del servicio de pagos. Implementar el patrón de retry asegura que, en lugar de rechazar el pago al primer fallo, el sistema reintente la operación después de un breve intervalo, aumentando así la probabilidad de éxito en la transacción.
		-   **Ventajas**: Minimiza la pérdida de ventas por problemas temporales y ofrece una experiencia de compra más fluida para los usuarios.
		
		#### 2. **Servicios de Streaming de Video**
		
		-   **Escenario**: Una plataforma de streaming, como Netflix, consulta constantemente un servicio de terceros para obtener recomendaciones personalizadas en tiempo real o para autenticar la sesión del usuario.
		-   **Uso del Patrón**: Durante momentos de alta demanda (picos de usuarios, como lanzamientos de episodios nuevos), estos servicios pueden experimentar latencia o fallos temporales. El patrón de retry permite que el sistema de recomendaciones o autenticación vuelva a intentar la consulta, evitando que el usuario vea un error en la pantalla o que se interrumpa la sesión.
		-   **Ventajas**: Mejora la continuidad del servicio y la experiencia de usuario, especialmente en situaciones de alta demanda.
		
		#### 3. **Sistemas de IoT y Telemetría Industrial**
		
		-   **Escenario**: Una empresa industrial utiliza sensores IoT para monitorear maquinaria y recopilar datos de rendimiento en tiempo real, los cuales se envían a una plataforma en la nube para análisis.
		-   **Uso del Patrón**: Los sensores envían datos periódicamente, pero debido a la latencia de red o congestión en la nube, algunas transmisiones pueden fallar. El patrón de retry permite que los dispositivos vuelvan a intentar el envío de datos después de un intervalo, asegurando que se capten y almacenen sin pérdida.
		-   **Ventajas**: Garantiza la integridad de los datos y permite que las alertas de mantenimiento o fallos en la maquinaria se procesen de forma precisa, evitando costosos tiempos de inactividad.
		
		#### 4. **Aplicaciones Financieras y Bancarias**
		
		-   **Escenario**: Un banco que procesa pagos entre cuentas nacionales e internacionales depende de servicios externos para verificar la identidad y el estado de cada transacción.
		-   **Uso del Patrón**: Si el sistema encuentra un error temporal al verificar una transacción o un servicio de validación de identidad, el patrón de retry permite que el sistema intente de nuevo antes de marcar la transacción como fallida. Esto puede ocurrir durante las horas pico cuando los servicios de validación están sobrecargados.
		-   **Ventajas**: Evita rechazos innecesarios de transacciones y proporciona una experiencia más confiable al cliente, especialmente en horarios críticos de procesamiento financiero.
		
		#### 5. **Mensajería en Tiempo Real (Ej. Slack o Microsoft Teams)**
		
		-   **Escenario**: En aplicaciones de colaboración en tiempo real, como Slack o Microsoft Teams, los mensajes deben ser entregados con rapidez y precisión, especialmente en sistemas distribuidos en múltiples regiones geográficas.
		-   **Uso del Patrón**: Durante el envío o recepción de mensajes, puede ocurrir una falla al intentar comunicarse con el servidor de mensajes. Con el patrón de retry, el cliente o el servidor intentan reenviar el mensaje hasta que sea entregado exitosamente.
		-   **Ventajas**: Reduce el riesgo de que los mensajes se pierdan por problemas temporales de red y mejora la experiencia de usuario, manteniendo la fiabilidad del sistema.
		
		#### 6. **Servicios de Marketing Basados en Eventos**
		
		-   **Escenario**: Una plataforma de marketing automatizado, como HubSpot, que envía notificaciones por correo electrónico o SMS a clientes según eventos de usuario.
		-   **Uso del Patrón**: Si un mensaje no se envía debido a una falla temporal en el proveedor de SMS o correo electrónico (como Twilio o SendGrid), el sistema aplica el patrón de retry para intentar enviar el mensaje otra vez. Este patrón es clave, especialmente durante campañas de marketing masivas en las que la tasa de fallos puede aumentar.
		-   **Ventajas**: Asegura que las notificaciones importantes lleguen al cliente y minimiza el impacto de fallos temporales en el proveedor de servicios, mejorando el alcance de las campañas.
		

   - **Aplicación en su Trabajo de Grupo**: En nuestro proyecto de grupo, el patrón Retry se podría aplicar en el módulo de estadísticas, reseñas y calificaciones. Este módulo permite a los usuarios autenticados visualizar el promedio de calificaciones y el total de reseñas de cada juego. Dado que el módulo necesita acceder constantemente a la base de datos para obtener estos datos, podrían surgir errores temporales que afecten la experiencia del usuario, como desconexiones o sobrecarga en la base de datos. Implementar Retry asegura que el sistema intente obtener los datos varias veces antes de fallar, minimizando el impacto de estos errores en la experiencia del usuario.

	    **Consideraciones a tener en cuenta**:
	
		-   **Configuración de intentos y tiempo de espera**: Es fundamental equilibrar la cantidad de intentos y el intervalo entre ellos. Un número alto de intentos o intervalos muy cortos puede sobrecargar aún más la base de datos.
		-   **Registro de errores**: Es importante llevar un registro de cuándo y por qué fallaron las solicitudes, ya que múltiples intentos fallidos pueden indicar un problema mayor que debe ser abordado.
		-   **Límite de uso del patrón**: Retry es ideal para errores transitorios, no para problemas constantes. Si la base de datos está caída por un tiempo prolongado, el patrón no resolverá el problema y el sistema puede terminar inoperativo.

**Diagrama de Patrón:**

![image](https://github.com/user-attachments/assets/fd690806-8068-4942-9313-137ceaadc019)

2. **Desarrollo de Código y Demo**:

   El escenario para la Demo es el siguiente: En el contexto de nuestro proyecto de aplicación o plataforma de recomendación de juegos, específicamente en el módulo de estadística, reseñas y calificaciones, tomamos una comunicación, particularmente la consulta por parte de la aplicación a la base de datos que aloja la información sobre calificaciones y reseñas, entonces la aplicación debe ser capaz de manejar fallos temporales de conexión o sobrecarga en base de datos. En esta demo se simulará una comunicación y se implementará el patrón Retry, en búsqueda de simular fallos y establecer reintentos de comunicación. Para la demo se establecerá un tiempo fijo entre intento e intento; sin embargo, se podrían configurar tiempos variables, y un cantidad máxima de reintentos de tres. Asimismo, se establecerá data de prueba y se implementará una simulación de fallas, mediante un valor aleatorio que simule que hay una falla temporal, es decir, cada vez que se intenta se genera un valor booleano que determina si hubo falla o no para regresar mensaje en consola, a continuación se muestra el paso a paso en código.

Pasos de la implementación:

   1.  **Instalación de la Librería Tenacity**:
    
-   **tenacity** es un paquete de Python que facilita la implementación del patrón Retry. Para instalarlo, ejecuta:
        
        `pip install tenacity` 
        
   2.  **Creación de la Función con Retry**:
	    
	    -   Implementamos la función `get_game_statistics`, que simula la consulta a la base de datos para obtener el promedio de calificaciones y el total de reseñas. Esta función usa `random.choice([True, False])` para simular la posibilidad de un fallo transitorio de conexión.

   3.  **Configuración de Retry**:
	    
	    -   Usamos el decorador `@retry` de `tenacity` para definir la cantidad de intentos y el tiempo de espera entre cada uno.
	    -   `wait_fixed(2)`: Cada intento espera un intervalo fijo de 2 segundos antes de reintentarlo.
	    -   `stop_after_attempt(3)`: Limita la cantidad de intentos a tres para evitar ciclos infinitos.

**Explicación Paso a Paso**:

-   **Paso 1**: `get_game_statistics` intenta conectarse a la base de datos. Si se produce un fallo (simulado aleatoriamente), `ConnectionError` es capturado y el Retry lo vuelve a intentar.
-   **Paso 2**: Si después de tres intentos el fallo persiste, se lanza un mensaje de error final.
-   **Resultado Final**: Si se obtiene una respuesta exitosa, se muestran el promedio de calificaciones y el total de reseñas. Si no se logra obtener los datos, se informa al usuario.

###Enlace a video de Demo en Youtube**
   **https://youtu.be/CCCPAA-gatM**
