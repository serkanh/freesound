package  {    import flash.events.Event;        /**     * @author bram     */    public class SoundManagerEvent extends Event     {    	public static const LOADING_PROGRESS_EVENT:String = "loading";    	public static const LOADING_FAILED_EVENT:String = "loadingFailed";    	public static const LOADING_COMPLETE_EVENT:String = "loadingComplete";    	    	public static const PLAY_EVENT:String = "play";    	public static const PLAYING_PROGRESS_EVENT:String = "playing";    	public static const PAUSE_EVENT:String = "pause";    	public static const STOP_EVENT:String = "stop";    	    	private var _procent:Number;    	        public function SoundManagerEvent(procent:Number, type : String, bubbles : Boolean = false, cancelable : Boolean = false)        {            super(type, bubbles, cancelable);                        _procent = procent;        }                public function get procent():Number        {        	return _procent;        }    }}