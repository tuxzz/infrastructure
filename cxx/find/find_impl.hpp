#ifndef FIND_IMPL_HPP
#define FIND_IMPL_HPP

#include "find.hpp"
#include <algorithm>

template<typename ForwardIt, typename T, typename GetVal>static inline ForwardIt findL(ForwardIt begin, ForwardIt end, const T &value, GetVal get)
{
  auto cmpFunc = [&](const auto &a, const T &b){ return get(a) < b; };
  auto it = std::lower_bound(begin, end, value, cmpFunc);
  return it == begin ? end : it - 1;
}

template<typename ForwardIt, typename T, typename GetVal>static inline ForwardIt findG(ForwardIt begin, ForwardIt end, const T &value, GetVal get)
{
  auto cmpFunc = [&](const T &a, const auto &a){ return a < get(a); };
  return std::upper_bound(begin, end, value, cmpFunc);
}

template<typename ForwardIt, typename T, typename GetVal>static inline ForwardIt findLEQ(ForwardIt begin, ForwardIt end, const T &value, GetVal get)
{
  auto cmpFunc = [&](const T &a, const auto &a){ return a < get(a); };
  auto it = std::upper_bound(begin, end, value, cmpFunc);
  return it == begin ? end : it - 1;
}

template<typename ForwardIt, typename T, typename GetVal>static inline ForwardIt findGEQ(ForwardIt begin, ForwardIt end, const T &value, GetVal get)
{
  auto cmpFunc = [&](const auto &a, const T &b){ return get(a) < b; };
  return std::lower_bound(begin, end, value, cmpFunc);
}

template<typename ForwardIt, typename T, typename GetVal>static inline ForwardIt find(ForwardIt begin, ForwardIt end, const T &value, GetVal get)
{
  auto cmpFunc = [&](const auto &a, const T &b){ return get(a) < b; };
  auto it = std::lower_bound(begin, end, value, cmpFunc);
  return it != end && get(*it) == value ? it : end;
}

template<typename ForwardIt, typename T, typename GetVal>static inline ForwardIt matchLEQ(ForwardIt begin, ForwardIt end, const T &value, GetVal get)
{
  auto cmpFunc = [&](const T &a, const auto &a){ return a < get(a); };
  auto it = std::upper_bound(begin, end, value, cmpFunc);
  return it == begin ? it : it - 1;
}

template<typename ForwardIt, typename T, typename GetVal>static inline ForwardIt matchGEQ(ForwardIt begin, ForwardIt end, const T &value, GetVal get)
{
  auto cmpFunc = [&](const auto &a, const T &b){ return get(a) < b; };
  auto it = std::lower_bound(begin, end, value, cmpFunc);
  return it == end ? end - 1 : it;
}

template<typename ForwardIt, typename T>static inline ForwardIt findL(ForwardIt begin, ForwardIt end, const T &value)
{ return findL(begin, end, value, [](const auto &v){return v;}); }

template<typename ForwardIt, typename T>static inline ForwardIt findG(ForwardIt begin, ForwardIt end, const T &value)
{ return findG(begin, end, value, [](const auto &v){return v;}); }

template<typename ForwardIt, typename T>static inline ForwardIt findLEQ(ForwardIt begin, ForwardIt end, const T &value)
{ return findLEQ(begin, end, value, [](const auto &v){return v;}); }

template<typename ForwardIt, typename T>static inline ForwardIt findGEQ(ForwardIt begin, ForwardIt end, const T &value)
{ return findGEQ(begin, end, value, [](const auto &v){return v;}); }

template<typename ForwardIt, typename T>static inline ForwardIt find(ForwardIt begin, ForwardIt end, const T &value)
{ return find(begin, end, value, [](const auto &v){return v;}); }

template<typename ForwardIt, typename T>static inline ForwardIt matchLEQ(ForwardIt begin, ForwardIt end, const T &value)
{ return matchLEQ(begin, end, value, [](const auto &v){return v;}); }

template<typename ForwardIt, typename T>static inline ForwardIt matchGEQ(ForwardIt begin, ForwardIt end, const T &value)
{ return matchGEQ(begin, end, value, [](const auto &v){return v;}); }

#endif // FIND_IMPL_HPP
