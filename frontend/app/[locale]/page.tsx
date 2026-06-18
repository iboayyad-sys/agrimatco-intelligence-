'use client'

import { useTranslations } from 'next-intl'
import Link from 'next/link'

export default function Home() {
  const t = useTranslations('home')

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-gray-900 dark:to-gray-800">
      {/* Navigation */}
      <nav className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-primary-600">🌾 Agrimatco</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/dashboard" className="btn btn-primary">
                {t('getStarted')}
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-gray-50 mb-6">
            {t('title')}
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto">
            {t('subtitle')}
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/auth/register" className="btn btn-primary text-lg px-8 py-3">
              {t('signUp')}
            </Link>
            <Link href="/auth/login" className="btn btn-outline text-lg px-8 py-3">
              {t('login')}
            </Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="bg-white dark:bg-gray-800 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h3 className="text-3xl font-bold text-center mb-12">{t('features')}</h3>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { icon: '📸', title: t('feature1Title'), desc: t('feature1Desc') },
              { icon: '🤖', title: t('feature2Title'), desc: t('feature2Desc') },
              { icon: '💊', title: t('feature3Title'), desc: t('feature3Desc') },
            ].map((feature, i) => (
              <div key={i} className="card text-center">
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h4 className="text-xl font-semibold mb-2">{feature.title}</h4>
                <p className="text-gray-600 dark:text-gray-400">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
