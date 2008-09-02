<xsl:stylesheet version="1.0"
   xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
   xmlns:h="http://www.w3.org/1999/xhtml">
   <xsl:output method="text" />
   <xsl:strip-space elements="*"/>

   <xsl:template match="h:form" >
      <xsl:if test="@action!=''">
Form/action: '<xsl:value-of select="@action" />'</xsl:if>
<xsl:if test="@name!=''">
Form/name: '<xsl:value-of select="@name" />'</xsl:if>
<xsl:if test="@id!=''">
Form/id: '<xsl:value-of select="@id" />'</xsl:if>
<xsl:if test="@title!=''">
Form/title: '<xsl:value-of select="@title" />'</xsl:if>
      <xsl:apply-templates />
      <xsl:text>
      </xsl:text>
   </xsl:template>

   <xsl:template match="h:input" >
      input/<xsl:value-of select="@type" /> { <xsl:if test="@title!=''">title: '<xsl:value-of select="@title" />',</xsl:if>
      <xsl:if test="@name!=''"> name: '<xsl:value-of select="@name" />',</xsl:if>
      <xsl:if test="@value!=''"> value: '<xsl:value-of select="@value" />',</xsl:if>
      <xsl:if test="@id!=''"> id: '<xsl:value-of select="@id" />'</xsl:if> }</xsl:template>

   <xsl:template match="h:textarea" >
      textarea { <xsl:if test="@title!=''">title: '<xsl:value-of select="@title" />',</xsl:if>
      <xsl:if test="@name!=''">name: '<xsl:value-of select="@name" />',</xsl:if>
      <xsl:if test="@value!=''">value: '<xsl:value-of select="@value" />',</xsl:if>
      <xsl:if test="@id!=''">id: '<xsl:value-of select="@id" />'</xsl:if> }</xsl:template>

   <xsl:template match="h:select" > 
      select { <xsl:if test="@name!=''">name: '<xsl:value-of select="@name" />',</xsl:if>
      <xsl:if test="@multiple">multiple: on, </xsl:if> options: { <xsl:apply-templates select="h:optgroup|h:option" /> } }</xsl:template>

   <xsl:template match="h:optgroup">
      '<xsl:value-of select="@label" />': { <xsl:apply-templates select="h:optgroup|h:option" /> }, </xsl:template>

   <xsl:template match="h:option">
      <xsl:choose>
         <xsl:when test="@label!=''">
            <xsl:if test="@selected">*</xsl:if>'<xsl:value-of select="@label" />', </xsl:when>
         <xsl:otherwise>
            <xsl:if test="@selected">*</xsl:if>'<xsl:value-of select="text()" />',  </xsl:otherwise>
      </xsl:choose>
   </xsl:template>

   <xsl:template match="text()|@*" />
</xsl:stylesheet>
