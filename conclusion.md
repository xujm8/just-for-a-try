# C++ 字符串题目总结
## 题目分析

该题目给了我们一个32位以内的魔法串，和不超过200个咒语，每个咒语都有对应的分数，咒语如果能匹配魔法串，则魔法串对应位置消失从而形成新的魔法串，魔法串的分数加上咒语相对应的分数。求魔法串能达到的最大分数和对应咒语消去的路径。

## 思路想法
*  思路一

    1. dfs暴力搜索，用Node存储路径，每个Node指向对应parent，自顶而下搜完后找到最大分数对应的叶子节点，输出分数和路径

    2. 结论：用一个32位的测试样例试了一下，需要超过1分钟 ，速度非常慢，于是想到了思路二


*  思路二

    1. 保留之前算过的魔法串，比如已知AABB的最优解是两个AB咒语，就用Path类记录该魔法串对应的最优咒语的路径，从而可以在下次同样遇到该魔法串时使用
    2. 使用递归的方式，findBest(原始串) = max[某个可匹配咒语的分数 + findBest(原始串-可匹配字符串)]。
    3. 保存路径的结构体Path为：
    ```
    struct Path{
        vector<string> spstr;
        vector<int> sppos;
        int val;
    };
    ```
    4. 结论：速度变为约1.6s左右，证明该方法可行。于是在这个基础上进行了改进。


    + 改进一：
        原匹配字符串和咒语部分：
        ```
        for (int i = 0; i < spellnum; ++ i) {
            int splen = allSpell[i].word.length();
            for (int j = 0; j <= rslen - splen; ++ j) {
                endFlag = 1;
                if (rsstr.substr(j,splen) == allSpell[i].word) {
                    ......
                }
            }
        }
        ```
        改进后：
        ```
        for (int i = 0; i < spellnum; ++ i) {
            int j = rsstr.find(allSell[i].word);
            while (j != string::npos) {
                ......
                j = rsstr.substr(j + 1).find(allSpell[i].word);
            }
        }
        ```
        从原来的逐个字符对比变为用find函数进行比较,用同样长度为32的测试数据测试，速度快了将近0.2s，这让我感觉奇怪，因为即使使用了kmp算法，在只有32位数据的情况下，也不可能优化这么多，于是我找到了string中find的源码
        ```
        template<typename _CharT, typename _Traits, typename _Alloc>
        typename basic_string<_CharT, _Traits, _Alloc>::size_type
        basic_string<_CharT, _Traits, _Alloc>::
        find(_CharT __c, size_type __pos) const
        {
            size_type __ret = npos;
            const size_type __size = this->size();
            if (__pos < __size)
            {
                const _CharT* __data = _M_data();
                const size_type __n = __size - __pos;
                const _CharT* __p = traits_type::find(__data + __pos, __n, __c);
                if (__p)
                    __ret = __p - __data;
            }
            return __ret;
        }

        static const char_type*
        find(const char_type* __s, size_t __n, const char_type& __a)
        {
            for (size_t __i = 0; __i < __n; ++__i)
            if (eq(__s[__i], __a))
                return __s + __i;
            return 0;
        }
        ```
        我发现string中find同样也是for循环逐个比较，那么这将近2s的多于开销，
        只能是''if (rsstr.substr(j,splen) == allSpell[i].word)''这个语句消耗的。find函数在for循环进行前将string转为了char*类型，而我频繁使用.substr函数，产生了大量开销。由此可见，string虽然方便，但是在速度方面比char\*慢了不少

    + 改进二
    
        由于对于每个出现过的路径，我都用两个vector存储了他们的咒语构成和每个咒语提取时对应的位置，占用了很多空间，于是我将Path结构体改为：
        ```
        struct Path{
            string spstr;
            int val;
        }
        ```
        每个spstr中存了对于路径，比如AABB路径是"1 AB,0 AB"，在输出时，用strtok分割字符串，从而输出路径。

        这样改我原本认为虽然减少了占用空间，但是由于输出的时候需要分割字符串，时间会增加，但是出乎我意料，不仅空间减小了，运行相同样例时，时间从1.4s降到了1.0s左右。后来思考后认为是vector的push_back太花时间，所以改为string后提速不少

    + 改进三
    
        用-O3编译后运行仅用0.4s，这个提升之大超乎我的想象。
    
        下面是O1,O2,O3优化的区别
        >O0选项不进行任何优化，在这种情况下，编译器尽量的缩短编译消耗（时间，空间），此时，debug会产出和程序预期的结果。当程序运行被断点打断，此时程序内的各种声明是独立的，我们可以任意的给变量赋值，或者在函数体内把程序计数器指到其他语句,以及从源程序中 精确地获取你期待的结果. 

        >O1优化会消耗少多的编译时间，它主要对代码的分支，常量以及表达式等进行优化。 

        >O2会尝试更多的寄存器级的优化以及指令级的优化，它会在编译期间占用更多的内存和编译时间。 

        >O3在O2的基础上进行更多的优化，例如使用伪寄存器网络，普通函数的内联，以及针对循环的更多优化。 

        优化可能带来的问题：
        1. 调试问题：正如上面所提到的，任何级别的优化都将带来代码结构的改变。例如：对分支的合并和消除，对公用子表达式的消除，对循环内load/store操作的替换和更改等，都将会使目标代码的执行顺序变得面目全非，导致调试信息严重不足。 

        2. 内存操作顺序改变所带来的问题：在O2优化后，编译器会对影响内存操作的执行顺序。例如：-fschedule-insns允许数据处理时先完成其他的指令；-fforce-mem有可能导致内存与寄存器之间的数据产生类似脏数据的不一致等。对于某些依赖内存操作顺序而进行的逻辑，需要做严格的处理后才能进行优化。
    
        防止问题发生的一些方法：
   
        - 采用volatile关键字限制变量的操作方式
        - 利用barrier迫使cpu严格按照指令序执行的。


## 帮助工具perf record perf report
可以看到cpu主要消耗在哪个函数中，着重对其进行优化，从而有效提高程序性能
