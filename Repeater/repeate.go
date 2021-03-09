package Repeater

import (
	"ProxyServer/Pkg"
	"fmt"
	"net/http"
	"net/http/httputil"
	"os"
	"strconv"
	"time"
)

const (
	delimeterReq="------------------REQUEST----------------------\n"
	delimeterResp="\n------------------RESPONSE----------------------\n"
)

func SaveReq(r *http.Request) (error, string){
	if r==nil{
		return nil, ""
	}
	file, err:=os.Create(getFileName(r.Method, Pkg.GetHost(r.Host)))
	if err!=nil{
		return err, ""
	}
	defer file.Close()
	isBodyEx:=true
	if r.Body==nil{
		isBodyEx=false
	}
	dumped:=delimeterReq+"<{["
	tmp, _:=httputil.DumpRequest(r, isBodyEx)
	dumped+=string(tmp)+"]}>"
	dumped+=delimeterResp
	file.WriteString(dumped)
	return  nil, getFileName(r.Method, Pkg.GetHost(r.Host))
}

func SaveResp(r *http.Response, filename string) error{
	if r==nil{
		return nil
	}
	file, err:=os.OpenFile(filename, os.O_APPEND|os.O_WRONLY, 0644)
	if err!=nil{
		return err
	}
	defer file.Close()
	isBodyEx:=true
	var t []byte
	n, _:=r.Body.Read(t)
	if n==0{
		isBodyEx=false
	}

	dumped:=delimeterResp
	tmp, err:=httputil.DumpResponse(r, isBodyEx)
	if err!=nil{
		fmt.Println("HUI:", err.Error())
		return err
	}
	dumped+=string(tmp)
	file.WriteString(dumped)
	return nil
}

func SaveRespstr(r string, filename string) error{
	file, err:=os.OpenFile(filename, os.O_APPEND|os.O_WRONLY, 0644)
	if err!=nil{
		return err
	}
	defer file.Close()

	file.WriteString(r)
	return nil
}

func getFileName(method string, url string) string{
	return "./Repeater/static/"+strconv.Itoa(int(time.Now().Unix()))+"_"+method+"_"+url+".txt"
}