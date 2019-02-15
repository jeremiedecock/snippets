package main

import "fmt"

func main() {

    a := []int{1, 2, 3, 4, 5, 6}

    for _, x := range a {
        fmt.Println(x)
    }

    for i, x := range a {
        fmt.Println(i, x)
    }

    m := map[string]int{"one": 1, "two": 2, "three": 3}

    for k, v := range m {
        fmt.Println(k, v)
    }

}

