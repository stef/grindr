<xsl:stylesheet version="1.0"
   xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
   xmlns:xupdate="http://www.xmldb.org/xupdate">
   <xsl:output method="text" />
   <xsl:template match="//xupdate:insert-after/xupdate:element" >
      <xsl:if test="@name='item'">
         <xsl:value-of select="../@select" />
         <xsl:text>&#10;</xsl:text>
      </xsl:if>
   </xsl:template>
   <xsl:template match="xupdate:append" />
   <xsl:template match="xupdate:comment" />
   <xsl:template match="text()|@*" />
</xsl:stylesheet>
