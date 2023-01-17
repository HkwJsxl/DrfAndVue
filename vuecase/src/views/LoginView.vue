<template>
  <div class="main">
    <div class="loginBox">
      <div class="tabBoxSwitch">
        <ul class="tabBoxSwitchUl">
          <li v-for="(item, index) in tabList" :key="index" :class="tabSelected === index?'tabActive':''"
              @click="tabSelected=index">
            {{ item }}
          </li>
        </ul>
      </div>
      <div class="formContent" v-show="tabSelected===0">
        <el-form class="demo-ruleForm" :model="userinfo" :rules="userinfoRules" ref="userinfo">
          <el-form-item prop="username">
            <el-input placeholder="用户名" v-model="userinfo.username"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input type="password" placeholder="密码" v-model="userinfo.password" autocomplete="off"
                      show-password></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="medium" @click="loginSubmit('userinfo')">提交</el-button>
          </el-form-item>
        </el-form>
      </div>
      <div class="formContent" v-show="tabSelected===1">
        <el-form class="demo-ruleForm" :model="userSms" type="flex" justify="space-between" :rules="userSmsRules"
                 ref="userSms">
          <el-form-item prop="mobile">
            <el-input v-model="userSms.mobile" placeholder="手机号"></el-input>
          </el-form-item>
          <el-form-item prop="code">
            <el-row type="flex" justify="space-between">
              <el-input v-model="userSms.code" placeholder="验证码"></el-input>
              <el-button style="margin-left: 24px" @click="sendSmsCode" :disabled="codeDisabled">{{ codeText }}</el-button>
            </el-row>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="medium" @click="loginSubmit('userSms')">提交</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoginView",
  data() {
    return {
      tabSelected: 1,
      tabList: ["密码登录", "免密码登录"],
      userinfo: {
        username: '',
        password: '',
      },
      userSms: {
        mobile: '',
        code: '',
      },
      userinfoRules: {
        username: [
          {required: true, message: '请输入用户名', trigger: 'blur'},
          {min: 3, max: 18, message: '长度在 3 到 18 个字符', trigger: 'blur'}
        ],
        password: [
          {required: true, message: '请输入密码', trigger: 'blur'},
          {min: 3, max: 18, message: '长度在 3 到 18 个字符', trigger: 'blur'}
        ]
      },
      userSmsRules: {
        mobile: [
          {required: true, message: '请输入手机号', trigger: 'blur'},
          {pattern: /^1[3456789]\d{9}$/, message: '手机号格式错误', trigger: 'blur'},
        ],
        code: [
          {required: true, message: '请输入验证码', trigger: 'blur'}
        ]
      },
      codeDisabled: false,
      codeText: '获取验证码',
    }
  },
  methods: {
    loginSubmit(dataRef) {
      this.$refs[dataRef].validate((valid) => {
        if (valid) {
          console.log('submit!');
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    sendSmsCode() {
      // 先验证手机号
      this.$refs.userSms.validateField("mobile", (error) => {
        if (error) {
          return false;
        }
        // 禁用按钮
        this.btnSmsDisabled = true;
        // 设置倒计时
        let codeBtnTxt = 60;
        let interval = window.setInterval(() => {
          this.codeText = `${codeBtnTxt}秒后重发`
          codeBtnTxt -= 1;
          if (codeBtnTxt < 1) {
            this.codeText = "重新发送";
            this.codeDisabled = false;
            window.clearInterval(interval);
          }
        }, 1000);
      })
    }
  }
}
</script>

<style scoped>
.main {
  width: 100%;
  height: 100vh;
  background-color: lightgray;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
}

.loginBox {
  width: 500px;
  height: 350px;
  background-color: #FFFFFF;
  box-shadow: 0 1px 3px rgba(26, 26, 26, 0.1);
}

.tabBoxSwitch .tabBoxSwitchUl li {
  display: inline-block;
  height: 70px;
  font-size: 16px;
  line-height: 70px;
  margin-left: 24px;
  cursor: pointer;
}

.tabActive {
  position: relative;
  color: #1a1a1a;
  font-weight: 700;
  font-synthesis: style;
}

.tabActive::before {
  display: block;
  position: absolute;
  bottom: 0;
  content: "";
  width: 100%;
  height: 3px;
  background-color: #0084ff;
}

.formContent {
  margin: 24px 24px 0;
}
</style>
