const plugin = require('tailwindcss/plugin')
const colors = require('tailwindcss/colors')

module.exports = {
  content: [
		"../static/js/**/*.{html,js}",
		"../templates/**/*.{html,js}",
		"../chat/**/*.{html,js}",
		"../contact/**/*.{html,js}",
		"../core/**/*.{html,js}",
		"../messagespaid/**/*.{html,js}",
		"../payment/**/*.{html,js}",
		"../user_profile/**/*.{html,js}",
  ],
	//purge: [],
	darkMode: false, // or 'media' or 'class'
	theme: {
		screens: {
			'sm': '640px',
			'md': '768px',
			'lg': '1024px',
			'xl': '1280px',
			'2xl': '1536px',
		},
		cursor: {
			auto: 'auto',
			default: 'default',
			pointer: 'pointer',
			wait: 'wait',
			text: 'text',
			move: 'move',
			'not-allowed': 'not-allowed',
			crosshair: 'crosshair',
			'zoom-in': 'zoom-in',
			'zoom-out': 'zoom-out',
		},
		extend: {
			height: {
				'128': '32rem',
			},
			colors: {
	      'primary': {
	        100: '#ffd372',
	        200: '#ffcb5b',
	        300: '#ffc443',
	        400: '#ffbc2c',
	        500: '#ffb514',
	        600: '#e6a312',
	        700: '#cc9110',
	        800: '#b37f0e',
	        900: '#996d0c',
	      },
	      'secondary': {
	        100: '#97e0f0',
	        200: '#85dbee',
	        300: '#74d5eb',
	        400: '#62d0e9',
	        500: '#51cbe6',
	        600: '#49b7cf',
	        700: '#41a2b8',
	        800: '#398ea1',
	        900: '#317a8a',
	      },
	      'tertiary': {
	        100: '#b5a7f3',
	        200: '#a392f0',
	        300: '#917cec',
	        400: '#6c50e6',
	        500: '#4724e0',
	        600: '#4020ca',
	        700: '#391db3',
	        800: '#32199d',
	        900: '#2b1686',
	      },
	      'quaternary': {
	        100: '#d7ceff',
	        200: '#d0c6ff',
	        300: '#c9bdff',
	        400: '#c3b5ff',
	        500: '#bcadff',
	        600: '#a99ce6',
	        700: '#968acc',
	        800: '#8479b3',
	        900: '#716899',
	      },
	      'quinary': {
        100: '#dcef8c',
        200: '#d6ec79',
        300: '#d1e965',
        400: '#cbe752',
        500: '#c5e43f',
        600: '#b1cd39',
        700: '#9eb632',
        800: '#8aa02c',
        900: '#768926',
      },
				stripe: {
					'400': '#5433FF',
					'600': '#2100cc'
				},
				paypal: {
					'400': '#0079C1',
					'600': '#00457C'
				},
	      gray: colors.zinc,
	      transparent: 'transparent',
	      current: 'currentColor',
	      'black': '#000000',
	      'white': '#ffffff',
	      emerald: colors.emerald,
	      indigo: colors.indigo,
	      yellow: colors.yellow,
	      red: colors.red,
	      orange: colors.orange,
	      green: colors.green,
	      purple: colors.purple,
				lime: colors.lime,
	      fuchsia: colors.fuchsia,
	      cyan: colors.cyan,
	      amber: colors.amber,
	      teal: colors.teal,
	      sky: colors.sky,
	      rose: colors.rose,
	      pink: colors.pink,
			},
			borderWidth: {
				'3': '3px',
			},
			inset: {
				'screen': '100vh',
				'-screen': '-100vh',
			},
			maxHeight: {
				'500': '500rem',
			},
			outline: {
				red: '2px solid #DC2626',
				gray: '2px solid #C0C0C0',
			},
			padding: {
				4.5: '1.125rem',
			},
			spacing: {
				4.5: '1.125rem',
				18: '4.5rem',
				128:'32rem',
			},
			transformOrigin: {
				'0': '0%',
			},
			zIndex: {
				'-1': '-1',
			},
			boxShadow: {
        'black': '8px 8px 0px 0px rgba(0, 0, 0, 1)',
        'black-left': '-8px 8px 0px 0px rgba(0, 0, 0, 1)'
      }
		},
	},
	variants: {
    backgroundColor: ({ after }) => after(['disabled']),
    textColor: ({ after }) => after(['disabled']),
    border: ({ after }) => after(['disabled']),
    borderColor: ({ after }) => after(['disabled']),
		// extend: {
		// 	borderWidth: ['hover', 'focus'],
		// 	padding: ['hover', 'focus'],
		// 	animation: ['hover', 'focus'],
		// 	scale: ['active'],
		// 	opacity: ['disabled'],
		// 	backgroundColor: ['disabled'],
		// 	textColor: ['disabled'],
		// 	borderColor: ['disabled'],
		// 	brightness: ['hover', 'focus'],
		// 	backgroundOpacity: ['disabled'],
		// }
	},
	plugins: [
		require('@tailwindcss/aspect-ratio'),
	],
}
