#include "gtest/gtest.h"
#include "simd_bits.h"
#include "simd_util.h"

TEST(simd_bits, move) {
    auto a = simd_bits(512);
    auto ptr = a.u64;
    simd_bits b = std::move(a);
    ASSERT_EQ(b.u64, ptr);
}

TEST(simd_bits, small_copy) {
    auto a = simd_bits(3);
    a.u64[0] = 1;
    auto b = a;
    ASSERT_EQ(b.u64[0], 1);
}

TEST(simd_bits, clear) {
    auto a = simd_bits::random(1001);
    ASSERT_TRUE(any_non_zero(a.u256, 4));
    a.clear();
    ASSERT_FALSE(any_non_zero(a.u256, 4));
}

TEST(simd_bits, bit_manipulation) {
    simd_bits a(1001);
    ASSERT_EQ(a.get_bit(300), false);
    a.set_bit(300, true);
    ASSERT_EQ(a.get_bit(300), true);
    a.set_bit(300, true);
    ASSERT_EQ(a.get_bit(300), true);
    a.set_bit(300, false);
    ASSERT_EQ(a.get_bit(300), false);
    a.toggle_bit_if(300, false);
    ASSERT_EQ(a.get_bit(300), false);
    a.toggle_bit_if(300, true);
    ASSERT_EQ(a.get_bit(300), true);
    a.toggle_bit_if(300, true);
    ASSERT_EQ(a.get_bit(300), false);
    a.toggle_bit_if(300, true);
    ASSERT_EQ(a.get_bit(300), true);
    a.toggle_bit_if(300, false);
    ASSERT_EQ(a.get_bit(300), true);
}