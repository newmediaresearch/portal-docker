FROM openjdk:7

EXPOSE 8080

ENV TOMCAT_VERSION 8.0.38
ENV ACTIVITI_VERSION 5.19.0
ENV POSTGRES_CONNECTOR_VERSION 42.2.2
ENV JYTHON_VERSION 2.7.0

# Tomcat
RUN wget http://archive.apache.org/dist/tomcat/tomcat-8/v${TOMCAT_VERSION}/bin/apache-tomcat-${TOMCAT_VERSION}.tar.gz -O /tmp/catalina.tar.gz && \
    tar xzf /tmp/catalina.tar.gz -C /opt && \
    ln -s /opt/apache-tomcat-${TOMCAT_VERSION} /opt/tomcat && \
    rm /tmp/catalina.tar.gz && \
    rm -rf /opt/tomcat/webapps/examples && \
    rm -rf /opt/tomcat/webapps/docs

# To install jar files first we need to deploy war files manually
RUN wget https://github.com/Activiti/Activiti/releases/download/activiti-${ACTIVITI_VERSION}/activiti-${ACTIVITI_VERSION}.zip -O /tmp/activiti.zip && \
    unzip /tmp/activiti.zip -d /opt/activiti && \
    unzip /opt/activiti/activiti-${ACTIVITI_VERSION}/wars/activiti-explorer.war -d /opt/tomcat/webapps/activiti-explorer && \
    unzip /opt/activiti/activiti-${ACTIVITI_VERSION}/wars/activiti-rest.war -d /opt/tomcat/webapps/activiti-rest && \
    rm -f /tmp/activiti.zip

# Add postgres connector to application
RUN wget https://jdbc.postgresql.org/download/postgresql-${POSTGRES_CONNECTOR_VERSION}.jre7.jar -O /tmp/postgresql-${POSTGRES_CONNECTOR_VERSION}.jre7.jar && \
    cp /tmp/postgresql-${POSTGRES_CONNECTOR_VERSION}.jre7.jar /opt/tomcat/webapps/activiti-rest/WEB-INF/lib/ && \
    cp /tmp/postgresql-${POSTGRES_CONNECTOR_VERSION}.jre7.jar /opt/tomcat/webapps/activiti-explorer/WEB-INF/lib/ && \
    rm -rf /tmp/postgresql-${POSTGRES_CONNECTOR_VERSION}.jre7.jar

# Add Jython to application
RUN wget http://search.maven.org/remotecontent?filepath=org/python/jython-standalone/${JYTHON_VERSION}/jython-standalone-${JYTHON_VERSION}.jar -O /tmp/jython-standalone-${JYTHON_VERSION}.jar && \
    mv /tmp/jython-standalone-${JYTHON_VERSION}.jar /opt/tomcat/lib/

# Add roles
ADD assets /assets
RUN mv /assets/config/tomcat/tomcat-users.xml /opt/tomcat/conf/

CMD ["/assets/init"]
