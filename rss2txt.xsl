<xsl:stylesheet
     version="1.0"
     xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
     <xsl:output method="xml" />
     <xsl:template match="rss/channel">
Feed Title: <xsl:value-of select="title" />
        <xsl:apply-templates select="title" />
        <xsl:apply-templates select="item" />
     </xsl:template>
     <xsl:template match="item">
------------------------------
Item title: <xsl:value-of select="title" />
Date: <xsl:value-of select="pubDate" /> 
<xsl:value-of select="description" />
     </xsl:template>
</xsl:stylesheet>
