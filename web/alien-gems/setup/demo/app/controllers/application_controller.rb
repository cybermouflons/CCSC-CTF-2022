class ApplicationController < ActionController::Base
  before_action :auth_me_pls

  def index
    @flag = ENV.fetch('SECRET_FLAG')
    unless session[:admin]
      @flag = "⛔"
    end
  end

  def auth_me_pls
    session[:admin] = true
    unless params[:token] == ENV.fetch('SECRET_TOKEN')
      session[:admin] = false
    end
  end
end
