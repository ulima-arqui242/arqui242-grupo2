
# Jean Pierre Soto Tipacti - Retry Pattern

1. **Desarrollo del Patrón**:
  
   - **Problema**
Una aplicación que se conecta con componentes cloud se espera que sea capaz de manejar o sobrellevar fallas transitorias que puedan ocurrir en este tipo de entornos, algunos de estas fallas pueden ser pequeñas interrupciones o pérdida temporal de conectividad a la red, una indisponibilidad del servicio o tiempos de espera que ocurren cuando un servicio se encuentra ocupado (usualmente, se da en servicios muy demandados que reciben múltiples solicitudes). Estas fallas típicamente se autocorrigen después de un tiempo, lo que lleva a que sea apropiado realizar una repetición del mismo llamado, por ejemplo, una base de datos que recibe múltiples solicitudes concurrentemente puede no responder a alguna, pero es factible que responda de realizar un nuevo intento después de un tiempo. Entonces, en resumen, se tiene un problema existente en posibles fallos temporales en algunos servicios que la aplicación requiere para su funcionamiento y que requieren de una solución.
  
   - **Solución**
El patrón Retry ofrece tres estrategias de solución, las cuales pueden ser aplicadas dependiendo del contexto de la aplicación, las estrategias son las siguientes:

		- Cancelar: Esta estrategia es recomendada cuando no se trata de un error transitorio y se encuentra poco probable que haya éxito en una repetición, en este caso se debería de cancelar la operación y enviar una excepción, por ejemplo, cuando busca realizar una autenticación y se tienen credenciales inválidas, por mucho que se reintente no se logrará tener éxito en la operación.
		
		- Reintentar: Esta estrategia se recomienda cuando la falla ocurre por una razón rara o inusual, podría haberse originado por circunstancias inusuales como una corrupción del paquete de red durante la transmisión, en este caso, se podría enviar la solicitud fallida nuevamente inmediatamente, puesto que se estima como poco probable que el error o falla vuelva a ocurrir, por lo que es muy factible que se tenga éxito.
		
		- Reintentar después de un retraso: Si la falla ocurrida es una de las fallas de conectividad o de ocupación más comunes, la red o el propio servicio podrían necesitar algo de tiempo mientras corrigen los problemas de conectividad o de ocupación. La aplicación debería esperar un tiempo antes de volver a enviar la solicitud, para las fallas más comunes se recomienda que se tenga estimado un periodo de tiempo entre reintentos para poder distribuir las solicitudes lo más uniformemente posible. Esto se realiza debido a que es más probable que el servicio se haya podido liberar de la sobrecarga, si reintentamos muy rápido y enviamos muchas solicitudes, no permitiremos que el servicio pueda liberarse de la sobrecarga. También se recomienda que  para esta estrategia se tenga un número de intentos limitados para que no se espere una respuesta eternamente ni se realicen reintentos infinitos. Por último, se debe considerar la existencia de un incremento exponencial entre los reintentos, pues no todas las fallas son iguales y podría existir alguna que necesito un poco más de tiempo, así que entre intento e intento sería conveniente que se apliquen periodos de tiempo que se vayan incrementando, por ejemplo entre el intento 1 y 2 se podría tener un tiempo de 2 segundos, y entre el intento 2 y 3 se podría tener un tiempo de 4 segundos.

   - **Casos de Aplicación**: Identifique y describa escenarios concretos y reales donde este patrón pueda aplicarse de forma efectiva. Considere casos de uso basados en la industria, aplicaciones empresariales, startups, etc.
   - **Aplicación en su Trabajo de Grupo**: Exponga cómo podría aplicarse el patrón en el proyecto grupal del curso, describiendo los beneficios y consideraciones que deben tenerse en cuenta.

2. **Desarrollo de Código y Demo**:
   - Implemente una solución que utilice el patrón seleccionado en un caso real o en un escenario de ejemplo bien definido.
   - Documente el caso real y detalle el proceso de implementación, asegurándose de describir cada paso realizado.
   - (Opcional) Prepare una demo en video donde muestre el funcionamiento de la implementación, explicando brevemente su funcionamiento.

3. **Entrega**:
   - Sobre su página personal en el repositorio de Github del grupo debe agregar una sección titulada "Patrones Cloud".
   - Puede desarrollar el código en el mismo repo o en un repositorio externo.
   - Si realiza el video, súbalo a una plataforma de su elección (YouTube, Vimeo, etc.) y comparta el enlace en la documentación.
