
com_list = [
	t('ul#example-1') > [
		t('li[v-for=item in items]', '{{item.message}}')
	],
	t('script') > [
	"""
	var example1 = new Vue({
			el: '#example-1',
			data: {
				items: [
					{message: 'foo'},
					{message: 'bar'}
				]	
			}
		})
	"""
	]
]
