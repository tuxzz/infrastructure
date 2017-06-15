#ifndef FIND_H
#define FIND_H

template<typename ForwardIt, typename T, typename GetVal>static inline ForwardIt findL(ForwardIt begin, ForwardIt end, const T &value, GetVal get);
template<typename ForwardIt, typename T, typename GetVal>static inline ForwardIt findG(ForwardIt begin, ForwardIt end, const T &value, GetVal get);
template<typename ForwardIt, typename T, typename GetVal>static inline ForwardIt findLEQ(ForwardIt begin, ForwardIt end, const T &value, GetVal get);
template<typename ForwardIt, typename T, typename GetVal>static inline ForwardIt findGEQ(ForwardIt begin, ForwardIt end, const T &value, GetVal get);
template<typename ForwardIt, typename T, typename GetVal>static inline ForwardIt find(ForwardIt begin, ForwardIt end, const T &value, GetVal get);
template<typename ForwardIt, typename T, typename GetVal>static inline ForwardIt matchLEQ(ForwardIt begin, ForwardIt end, const T &value, GetVal get);
template<typename ForwardIt, typename T, typename GetVal>static inline ForwardIt matchGEQ(ForwardIt begin, ForwardIt end, const T &value, GetVal get);
template<typename ForwardIt, typename T>static inline ForwardIt findL(ForwardIt begin, ForwardIt end, const T &value);
template<typename ForwardIt, typename T>static inline ForwardIt findG(ForwardIt begin, ForwardIt end, const T &value);
template<typename ForwardIt, typename T>static inline ForwardIt findLEQ(ForwardIt begin, ForwardIt end, const T &value);
template<typename ForwardIt, typename T>static inline ForwardIt findGEQ(ForwardIt begin, ForwardIt end, const T &value);
template<typename ForwardIt, typename T>static inline ForwardIt find(ForwardIt begin, ForwardIt end, const T &value);
template<typename ForwardIt, typename T>static inline ForwardIt matchLEQ(ForwardIt begin, ForwardIt end, const T &value);
template<typename ForwardIt, typename T>static inline ForwardIt matchGEQ(ForwardIt begin, ForwardIt end, const T &value);

#include "find_impl.hpp"

#endif // FIND_H
