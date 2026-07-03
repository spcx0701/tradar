package kr.tradewind.app.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class WatchlistStoreTest {
    @Test
    fun togglesHsCodesWithoutDuplicates() {
        val store = WatchlistStore(InMemoryKeyValueStore())

        assertTrue(store.toggle("1902.30"))
        assertFalse(store.toggle("1902.30"))
        store.add("3304.99")
        store.add("1212.21")
        store.add("3304.99")

        assertEquals(listOf("1212.21", "3304.99"), store.savedHsCodes())
        assertTrue(store.isSaved("3304.99"))
        assertFalse(store.isSaved("1902.30"))
    }

    @Test
    fun persistsStablePipeDelimitedValue() {
        val backing = InMemoryKeyValueStore()
        val first = WatchlistStore(backing)

        first.add("3304.99")
        first.add("1902.30")

        assertEquals("1902.30|3304.99", backing.getString("watchlist_hs_codes").orEmpty())
        assertEquals(listOf("1902.30", "3304.99"), WatchlistStore(backing).savedHsCodes())
    }
}
