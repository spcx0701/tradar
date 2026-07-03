package kr.tradewind.app.data

import android.content.SharedPreferences

interface KeyValueStore {
    fun getString(key: String): String?
    fun putString(key: String, value: String)
}

class SharedPreferencesKeyValueStore(private val preferences: SharedPreferences) : KeyValueStore {
    override fun getString(key: String): String? = preferences.getString(key, null)

    override fun putString(key: String, value: String) {
        preferences.edit().putString(key, value).apply()
    }
}

class InMemoryKeyValueStore : KeyValueStore {
    private val values = mutableMapOf<String, String>()

    override fun getString(key: String): String? = values[key]

    override fun putString(key: String, value: String) {
        values[key] = value
    }
}

class WatchlistStore(
    private val keyValueStore: KeyValueStore,
    private val key: String = WATCHLIST_KEY,
) {
    fun savedHsCodes(): List<String> =
        keyValueStore.getString(key)
            .orEmpty()
            .split("|")
            .map { it.trim() }
            .filter { it.isNotBlank() }
            .distinct()
            .sorted()

    fun isSaved(hs: String): Boolean = hs in savedHsCodes()

    fun add(hs: String) {
        write(savedHsCodes() + hs)
    }

    fun remove(hs: String) {
        write(savedHsCodes().filterNot { it == hs })
    }

    fun toggle(hs: String): Boolean {
        val saved = savedHsCodes()
        return if (hs in saved) {
            write(saved.filterNot { it == hs })
            false
        } else {
            write(saved + hs)
            true
        }
    }

    private fun write(values: List<String>) {
        keyValueStore.putString(key, values.map { it.trim() }.filter { it.isNotBlank() }.distinct().sorted().joinToString("|"))
    }

    private companion object {
        const val WATCHLIST_KEY = "watchlist_hs_codes"
    }
}
