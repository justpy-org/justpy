function    createApp() {
        var app1 = new Vue({
            el: '#components',
            data: {
                justpyComponents: justpyComponents
            },
            render: function (h) {
                var comps = [];
                for (var i = 0; i < this.justpyComponents.length; i++) {
                    if (this.justpyComponents[i].show) {
                        comps.push(h(this.justpyComponents[i].vue_type, {
                            props: {
                                jp_props: this.justpyComponents[i]
                            }
                        }))
                    }
                }
                return h('div', {}, comps);
            }
        });
  return app1;
}
