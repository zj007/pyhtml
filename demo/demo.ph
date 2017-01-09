head = load('head')

def div_c():
	return 'div_c'

div_class = 'div1'

html = t('html') > [
			
			t('head') > [
				head['head_base'],

				t('title', 'pyhtml')
			],

			t('body') > [
				t('h1', 'demo'),

				t('p', 'a text') > [t('scan', 'a')],
				
				#for
				t('ul') > [
					[t('li', i) for i in xrange(2)],
				],
				
				t('div.{}'.format(div_class), div_c()),
				
				#if
				t('div') if False else [],
				
			]	
	   ]
