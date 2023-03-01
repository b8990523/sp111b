#include <stdio.h>

/*double (*f)(double) 是个函数指针，f就是一个指针变量，可以指向返回double，参数是double 的函数
  所以會帶入square函數
*/

double integrate(double (*f)(double),double a, double b) {
    double step = 0.001, sum=0.0;
    for (double x=a; x<b; x+=step){ /*step表示a、b之間的分段，數值越小越精確*/
        sum += f(x)*step;
    }
    return sum;
}

double square(double x) {
    // 定義需要積分的函數，這邊定義x^2
    return x*x;
}

int main() {
    // 計算 x^2 在區間 [0, 2] 的積分
    printf("integrate(square, 0.0, 2.0)=%f\n", integrate(square, 0.0, 2.0));
}
