head = load('head')
reverse_com = load('reverse_com')
com_list = load('com_list')

html = t('html') > [
			t('head') > [
				head['vue'],
				t('title', 'pyhtml'),
			],

			t('body') > [
				t('h1', 'demo'),
				reverse_com['reverse_com'],
				com_list['com_list'],
			]	
	   ]
