import justpy as jp

link_classes='m-2 bg-blue-500 hover:bg-blue-700 text-white font-bold p-2 rounded'
print(globals())
# jp.FePointLight()
# jp.FeSpecularLighting()
def link_demo():
    wp = jp.WebPage()
    root = jp.Div(name='root', a=wp)
    c1 = jp.Svg(height='200', width='200', viewBox='0 0 220 220', xmlns='http://www.w3.org/2000/svg', a=root)
    c2 = jp.Filter(a=c1)
    c3 = jp.FeSpecularLighting(result='specOut', specularExponent='20', lighting_color='#bbbbbb', a=c2)
    c4 = jp.FePointLight(x='50', y='75', z='200', a=c3)
    c5 = jp.FeComposite(_in='SourceGraphic', in2='specOut', operator='arithmetic', k1='0', k2='1', k3='1', k4='0', a=c2)
    c6 = jp.Circle(cx='110', cy='110', r='100', style=f'filter:url(#{c2.id})', a=c1)
    # link = jp.A(text='Python', href='https://python.org', a=wp, classes='m-2 p-2 underline text-2xl text-blue-500 visited:text-green-500')
    # link.target = '_blank'
    d2 = jp.parse_html_file("C:\\Users\\eli\\PycharmProjects\\StarPy\\tests\\misc\\svg_tiger.html", a=wp)
    g = jp.parse_html("""
    <svg height="200" width="200" viewBox="0 0 220 220"
    xmlns="http://www.w3.org/2000/svg">
  <filter id = "filter">
    <feSpecularLighting result="specOut"
        specularExponent="20" lighting-color="#bbbbbb">
      <fePointLight x="50" y="75" z="200"/>
    </feSpecularLighting>
    <feComposite _in="SourceGraphic" in2="specOut"
        operator="arithmetic" k1="0" k2="1" k3="1" k4="0"/>
  </filter>
  <circle cx="110" cy="110" r="100" style="filter:url(#2)"/>
</svg>
    """, a=wp)
    # g.add_to(wp)

    g = jp.parse_html("""
        <svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" width="240" height="240">
  <path d="M 10,30
           A 20,20 0,0,1 50,30
           A 20,20 0,0,1 90,30
           Q 90,60 50,90
           Q 10,60 10,30 z" fill="pink">
           <animateTransform attributeName="transform"
                          attributeType="XML"
                          type="rotate"
                          from="0 60 60"
                          to="360 60 60"
                          dur="10s"
                          repeatCount="indefinite"/>
           </path>
</svg>
        """, a=wp)
    # g.add_to(wp)
    g.classes='m-4 p-4'
    def heart_click(self, msg):
        if self.fill == 'blue':
            self.fill = 'pink'
            self.components[0].dur = '10s'
        else:
            self.fill = 'blue'
            self.components[0].dur = '1s'
    g.components[0].on('click', heart_click)
    g = jp.parse_html("""
            <svg width="120" height="120" viewBox="0 0 120 120"
              class="inline-block">

            <polygon points="0,120 0,30 30,30 30,0" fill="red">

            </polygon>
        </svg>
            """, a=wp)
    # g.add_to(wp)
    g = jp.parse_html("""
    <svg width="120" height="120" viewBox="0 0 120 120"
     xmlns="http://www.w3.org/2000/svg"  class="inline-block">

    <polygon points="60,30 90,90 30,90" fill="red">
        <animateTransform attributeName="transform"
                          attributeType="XML"
                          type="rotate"
                          from="0 60 70"
                          to="360 60 70"
                          dur="10s"
                          repeatCount="indefinite"/>
    </polygon>
</svg>
    """, a=wp)
    # g.add_to(wp)
    g = jp.parse_html("""
        <svg width="120" height="120" viewBox="0 0 120 120"
         xmlns="http://www.w3.org/2000/svg" class="inline-block">

        <polygon points="60,60 90,90 30,90" fill="red">
            <animateTransform attributeName="transform"
                              attributeType="XML"
                              type="rotate"
                              from="0 60 70"
                              to="360 60 70"
                              dur="10s"
                              repeatCount="indefinite"/>
        </polygon>
    </svg>
        """, a=wp)
    # g.add_to(wp)

    return wp
    l = jp.parse_html("""
    <p>You can reach Michael at:</p>

<ul>
  <li ><a name=li1 href="https://example.com">Website</a></li>
  <li><a name=li2 href="mailto:m.bluth@example.com">Email</a></li>
  <li ><a name=li3 href="tel:+123456789">Phone</a></li>
  <li ><a name=li4 href="http://python.org">python</a></li>
</ul>
    """)
    print(l.name_dict)
    print(list(l.name_dict.values()))
    for c in list(l.name_dict.values()):
        print(c)
        print(c.href)
    # l.name_dict['li1'].href = "tel:+123456789"
    return wp

jp.justpy(link_demo)


