
reverse_com = [
				t('div#app-5') > [
					t('p', '{{message}}'),
					t('button[v-on:click=reverseMessage]', 'Reverse Message'),
				],
				t('script') > [
					"""
					var app5 = new Vue({
							el: '#app-5',
							data: {
								message: 'Hello Vue.js'
								},
							methods: {
								reverseMessage: function() {
									 this.message = this.message.split('').reverse().join('')
									}
								}
						})
					"""
				]
]
